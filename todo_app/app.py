from todo_app.data import session_items
from flask import Flask, render_template,redirect,url_for
from flask.globals import request
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=["GET"])
def index_get():
    items =  session_items.get_items()
    return render_template('index.html',items=items)

@app.route('/delete', methods=["POST"])
def delete_item():
    val = request.form.get("deletebutton")
    session_items.delete_item(val)
    return redirect(url_for('index_get'))

@app.route('/reset', methods=["POST"])
def reset_item():
    val = request.form.get("Reset")
    session_items.change_status_item(val,False)
    return redirect(url_for('index_get'))

@app.route('/complete', methods=["POST"])
def complete_item():
    val = request.form.get("Complete")
    session_items.change_status_item(val,True)
    return redirect(url_for('index_get'))


@app.route('/additem', methods=["POST"])
def add_item():
    val = request.form.get("data")
    session_items.add_item(val)
    return redirect(url_for('index_get'))

if __name__ == '__main__':
    app.run()
