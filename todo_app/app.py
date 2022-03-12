import os,pymongo,json
import logging,sys
from todo_app.Auth.user import User
from todo_app.data import session_items
from flask import Flask, render_template,redirect,url_for
from flask.globals import request
import requests
from todo_app.data.itemstatus import ItemStatus
from todo_app.model.viewModel import ViewModel
from oauthlib.oauth2 import WebApplicationClient
from flask_login import login_required,LoginManager,login_user,current_user
users = {'None':User()}

def get_DB():
    client = pymongo.MongoClient(f"{os.getenv('MONGO_CONNECTION_STRING')}")
    db = client["db"]
    col = os.getenv('TRELLO_BOARD')
    return db[col]
    
def del_DB(db):
    db.drop()

def create_app(db = None):
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED')
    logging.basicConfig(level = os.getenv('LOG_LEVEL')) 
    mylog = logging.getLogger('todoapp')
    
    if db == None:
        db = get_DB()

    #login manager
    login_manager = LoginManager()
    mylog.info('Creating WebClient')
    client = WebApplicationClient(os.getenv('GITHUB_CLIENTID'))

    @login_manager.unauthorized_handler
    def unauthenticated():
        mylog.debug('User being redirected to github')
        authorization_endpoint = 'https://github.com/login/oauth/authorize'
        request_uri = client.prepare_request_uri(
            authorization_endpoint
        )
        return redirect(request_uri)

    @login_manager.user_loader
    def load_user(user_id):
        mylog.debug('Obtaining User details')
        if user_id in users:
            return users[user_id] 
        else:
            return None


    login_manager.init_app(app)
    mylog.info('App up and working.')
    @app.route('/users/callback', methods=["GET"])
    def callback_func():
        mylog.debug('Github Oath callback')
        token_endpoint='https://github.com/login/oauth/access_token'
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            client_secret=os.getenv('GITHUB_CLIENTSECRET')
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body
        )
        # Parse the tokens!
        client.parse_request_body_response(token_response.content.decode())
        
        # get user details
        userinfo_endpoint = 'https://api.github.com/user'
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.json().get("login"):
            mylog.debug('User ' + userinfo_response.json().get("login") + 'has being redirected from github.')
            login = userinfo_response.json()["login"]
            unique_id = userinfo_response.json()["id"]
            email = userinfo_response.json()["email"]
            avatar = userinfo_response.json()["avatar_url"]
        else:
            return "User email not available or not verified by Github.", 400
        user = User(unique_id,login, email, avatar)
        if login_user(user):
            users[str(unique_id)] = user
        #Redirection to main page, if user did not authenticated well, it will be redirected again to github.
        return redirect(url_for("index_get"))

    @app.route('/')
    @login_required
    def index_get():
        items =  session_items.get_items(db)
        item_view_model = ViewModel(items,users[str(current_user.get_id())])
        return render_template('index.html',view_model=item_view_model)

    @app.route('/delete', methods=["POST"])
    @login_required
    def delete_item():
        
        if users[str(current_user.get_id())].isWriter():
            val = request.form.get("deletebutton")
            mylog.debug('User:' + users[str(current_user.get_id())].name + ' is trying to delete  item ' + val)
            session_items.delete_item(db,val)
            return redirect(url_for('index_get'))
        else:    
            mylog.error('User:' + users[str(current_user.get_id())].name + ' is trying to delete  item but it is now authorized.')

    @app.route('/reset', methods=["POST"])
    @login_required
    def reset_item():
        if users[str(current_user.get_id())].isWriter():
            val = request.form.get("Reset")
            session_items.change_status_item(db,val,ItemStatus.TODO)
            return redirect(url_for('index_get'))

    @app.route('/complete', methods=["POST"])
    @login_required
    def complete_item():
        if users[str(current_user.get_id())].isWriter():
            val = request.form.get("Complete")
            session_items.change_status_item(db,val,ItemStatus.FINISHED)
            return redirect(url_for('index_get'))

    @app.route('/doing', methods=["POST"])
    @login_required
    def doing_item():
        if users[str(current_user.get_id())].isWriter():
            val = request.form.get("Doing")
            session_items.change_status_item(db,val,ItemStatus.DOING)
            return redirect(url_for('index_get'))

    @app.route('/additem', methods=["POST"])
    @login_required
    def add_item():
        if users[str(current_user.get_id())].isWriter():
            val = request.form.get("data")
            session_items.add_item(db,val)
            return redirect(url_for('index_get'))
    return app

if __name__ == '__main__':
    create_app().run()

