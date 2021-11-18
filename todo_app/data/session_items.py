from flask import session
import json,requests,uuid,os,uuid
from bson.objectid import ObjectId
from todo_app.data import itemstatus
from todo_app.data.item import Item
from todo_app.data.itemstatus import ItemStatus

def get_items(db):
    items = []
    for item in db.find():
        items.append(
            Item(
                item['_id'],
                ItemStatus(item['status']),
                item['title']
            )
        )
    return sorted(items, key=lambda k: k.status.value)


def delete_item(db,id):
    db.delete_one({ '_id': ObjectId(id) })
    return

def add_item(db,title):
    db.insert_one(
        {
            "title": title,
            "status": ItemStatus.TODO.value,
            "card_id": uuid.uuid4()
        }
    )
    return
def change_status_item(db,id,newStatus):
    db.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "status": newStatus.value
            }
        }
    )

    return
