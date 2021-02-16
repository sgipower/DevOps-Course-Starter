from todo_app.data import session_items
from flask import Flask, render_template
from flask.globals import request, session

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=["GET"])
def index_get():
    items =  session_items.get_items()
    return render_template('index.html',items=items)


@app.route('/', methods=["POST"])
def edit_item():
    if "deletebutton" in request.form:
        val = request.form.get("deletebutton")
        print(val)
        session_items.delete_item(val)
    elif "Complete" in request.form:
        val = request.form.get("Complete")
        item = session_items.get_item(int(val))
        item['status'] = "Completed"
        session_items.save_item(item)
    elif "Reset" in request.form:
        val = request.form.get("Reset")
        item = session_items.get_item(int(val))
        item['status'] = "Not Started"
        session_items.save_item(item)
    items =  session_items.get_items()
    return render_template('index.html',items=items)


@app.route('/additem', methods=["POST"])
def add_item():
    val = request.form.get("data")
    print(val)
    session_items.add_item(val)
    items =  session_items.get_items()
    return render_template('index.html',items=items)

if __name__ == '__main__':
    app.run()
