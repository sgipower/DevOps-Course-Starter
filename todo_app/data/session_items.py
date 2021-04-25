from flask import session
import json,requests,uuid,os
from todo_app.data.item import Item
from todo_app.data.itemstatus import ItemStatus

def init_board():
    boardID = os.environ.get('TRELLO_BOARD')
    #CHECK BOARD EXISTS
    r = requests.get('https://api.trello.com/1/boards/' + boardID , data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')})
    if r.status_code == 200:
        print("Board found on Trello.")
        session['boardId'] = boardID
        init_lists()
        return
    else:
        print("Error finding the board.Going to create one. Error:" + r.reason)

    r = requests.post('https://api.trello.com/1/boards/', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'name':'DevOps-Course-Starter','defaultLists':'false'})
    if r.status_code != 200:
        print("Error creating a brand new board board.Probably you have reached the maximum. Error:" + r.reason)
        return
    else:
        session['boardId'] = r.json()['id']
        print("The board configured on .env is not valid or does not exist. Please to persist it, add the new board to your .env file:\r\nTRELLO_BOARD="+ r.json()['id'])
        init_lists()
    
def init_lists():
    boardID = session.get('boardId', "")
      #get lists on the board
    r = requests.get('https://api.trello.com/1/boards/' + boardID  + '/lists', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN')})
    if r.status_code == 200:
        print("Retrieved lists:" + r.text )
        for listnameItem in ItemStatus:
            listname = listnameItem.name
            res = next((sub for sub in r.json() if sub['name'] == listname), None)
            if res != None:
                print('listing found:' + listname + " : "+ res['id'])
                session[listname] = res['id']
            else:
                print("creating listings:" + listname)
                rr = requests.post('https://api.trello.com/1/boards/' + boardID + '/lists', data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'name':listname})
                if rr.status_code != 200:
                    print("Error creating list: " + listname +". Error:" + rr.reason)
                    return
                else:
                    listid = rr.json()['id']
                    session[listname] = listid
    else:
        raise Exception("Cannot get a list of lists from the boardid" + boardID)

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
            elif idList == session[ItemStatus.DOING.name]:
                status = ItemStatus.DOING
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
    print("status:" + session[newStatus.name])
    r = requests.put('https://api.trello.com/1/cards/'+ id, data = {'key':os.environ.get('TRELLO_KEY'),'token':os.environ.get('TRELLO_TOKEN'),'idList':session[newStatus.name] })
    print(r.url)
    if r.status_code != 200:
        print("Error changing card. Error:" + r.reason)
    return
