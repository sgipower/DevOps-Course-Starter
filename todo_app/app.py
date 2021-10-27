import os,pymongo
from todo_app.data import session_items
from flask import Flask, render_template,redirect,url_for
from flask.globals import request
from todo_app.data.itemstatus import ItemStatus
from todo_app.model.viewModel import ViewModel

def get_DB():
    client = pymongo.MongoClient(f"mongodb+srv://{os.getenv('MONGO_USERNAME')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST')}/?w=majority")
    db = client[os.getenv('DEFAULT_DATABASE')]
    col = os.getenv('TRELLO_BOARD')
    return db[col]
    
def del_DB(db):
    db.drop()

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    db = get_DB()

    @app.route('/', methods=["GET"])
    def index_get():
        items =  session_items.get_items(db)
        item_view_model = ViewModel(items)
        return render_template('index.html',view_model=item_view_model)

    @app.route('/delete', methods=["POST"])
    def delete_item():
        val = request.form.get("deletebutton")
        session_items.delete_item(db,val)
        return redirect(url_for('index_get'))

    @app.route('/reset', methods=["POST"])
    def reset_item():
        val = request.form.get("Reset")
        session_items.change_status_item(db,val,ItemStatus.TODO)
        return redirect(url_for('index_get'))

    @app.route('/complete', methods=["POST"])
    def complete_item():
        val = request.form.get("Complete")
        session_items.change_status_item(db,val,ItemStatus.FINISHED)
        return redirect(url_for('index_get'))

    @app.route('/doing', methods=["POST"])
    def doing_item():
        val = request.form.get("Doing")
        session_items.change_status_item(db,val,ItemStatus.DOING)
        return redirect(url_for('index_get'))

    @app.route('/additem', methods=["POST"])
    def add_item():
        val = request.form.get("data")
        session_items.add_item(db,val)
        return redirect(url_for('index_get'))
    return app

if __name__ == '__main__':
    create_app().run()

