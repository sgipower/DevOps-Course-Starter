from flask import session
import json,requests,uuid,os
from enum import Enum

class Lists(Enum):
    TODO = 1
    FINISHED = 2

class Item:
    def __init__(self,id = None,status=None,title=None,cardid=None):
        self.id= id if id is not None else -1
        self.status= status if status is not None else Lists.TODO
        self.title= title if title is not None else 'List saved todo items'
        self.cardid= cardid
    def unstarted(self):
        return self.status == Lists.TODO.value
    def description(self):
        return Lists(self.status).name  
    def __str__(self):
     return "id:" + str(self.id)  

def init_board():
    boardName = uuid.uuid4().hex
    r = requests.post('https://api.trello.com/1/boards/', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'name':boardName,'defaultLists':'false'})
    if r.status_code != 200:
        print("Error creating a brand new board board. Error:" + r.reason)
        return
    else:
        boardId = r.json()['id']
        session['boardId'] = boardId
    for listnameItem in Lists:
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
            if idList == session[Lists.TODO.name]:
                desc = Lists.TODO.value
            elif idList == session[Lists.FINISHED.name]:
                desc = Lists.FINISHED.value
            else:
                desc = -1

            items.append(Item(int(card['idShort']),desc,card['name'],card['id']))
    return sorted(items, key=lambda k: k.status)


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
    r = requests.post('https://api.trello.com/1/cards/', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'name':title , 'idList':session[Lists.TODO.name] })
    if r.status_code != 200:
        print("Error creating card. Error:" + r.reason)
    return
def change_status_item(id,completed):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    if completed:
        status  = Lists.FINISHED.name
    else:
        status = Lists.TODO.name
    r = requests.put('https://api.trello.com/1/cards/'+ id, data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'idList':session[status] })
    if r.status_code != 200:
        print("Error changing card. Error:" + r.reason)
    return

    return item
