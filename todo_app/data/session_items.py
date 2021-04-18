from flask import session
import json,requests,uuid,os
from todo_app.data.item import Item
from todo_app.data.itemstatus import ItemStatus

def init_board():
    boardName = os.environ.get('TRELLO_BOARD')
    #CHECK BOARD EXISTS
    r = requests.get('https://api.trello.com/1/boards/', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'id ':boardName})
    if r.status_code == 200:
        print("Board found on Trello.")
        session['boardId'] = boardName
        return

    r = requests.post('https://api.trello.com/1/boards/', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'name':boardName,'defaultLists':'false'})
    if r.status_code != 200:
        print("Error creating a brand new board board. Error:" + r.reason)
        return
    else:
        boardId = r.json()['id']
        session['boardId'] = boardId
    for listnameItem in ItemStatus:
        listname = listnameItem.name
        print("creating listings:" + listname)
        r = requests.post('https://api.trello.com/1/boards/' + boardId + '/lists', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'name':listname})
        if r.status_code != 200:
            print("Error creating list: " + listname +". Error:" + r.reason)
            return
        else:
            listid = r.json()['id']
            session[listname] = listid

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    items = []
    boardId = session.get('boardId', "")
    if boardId == "":
        init_board()       
    boardId = session.get('boardId', "")
    #get list of items.
    r = requests.get('https://api.trello.com/1/boards/' + boardId + '/cards', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')})
    if r.status_code != 200:
            print("Error getting cards. Error:" + r.reason)
            return
    else:
        
        for card in r.json():
            idList = card['idList']
            if idList == session[ItemStatus.TODO.name]:
                status = ItemStatus.TODO
            elif idList == session[ItemStatus.FINISHED.name]:
                status = ItemStatus.FINISHED
            else:
                status = -1

            items.append(Item(int(card['idShort']),status,card['name'],card['id']))
    return sorted(items, key=lambda k: k.status.value)


def delete_item(id):
    r = requests.delete('https://api.trello.com/1/cards/' + id, data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')})
    if r.status_code != 200:
        print("Error deleting card. Error:" + r.reason)
    return

def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.  
    """
    r = requests.post('https://api.trello.com/1/cards/', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'name':title , 'idList':session[ItemStatus.TODO.name] })
    if r.status_code != 200:
        print("Error creating card. Error:" + r.reason)
    return
def change_status_item(id,newStatus):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    r = requests.put('https://api.trello.com/1/cards/'+ id, data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'idList':session[newStatus.name] })
    if r.status_code != 200:
        print("Error changing card. Error:" + r.reason)
    return
