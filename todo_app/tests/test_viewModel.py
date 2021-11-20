from todo_app.Auth.user import User
from todo_app.data import itemstatus
from todo_app.data.itemstatus import ItemStatus
from todo_app.model.viewModel import ViewModel
from todo_app.data.item import Item

def test_CheckTodoList():
    items = []
    items.append(Item(1,ItemStatus.TODO))

    view = ViewModel(items,User())

    assert  len(view.todo_items) == 1 
    assert  len(view.finished_items) == 0
    assert  len(view.doing_items) == 0 
    assert view.has_todo_items == True
    assert view.has_doing_items == False
    assert view.has_finished_items == False

def test_CheckDoingList():
    items = []
    items.append(Item(1,ItemStatus.DOING))

    view = ViewModel(items,User())

    assert  len(view.todo_items) == 0 
    assert  len(view.finished_items) == 0
    assert  len(view.doing_items) == 1
    assert view.has_todo_items == False
    assert view.has_doing_items == True
    assert view.has_finished_items == False

def test_CheckDoneList():
    items = []
    items.append(Item(1,ItemStatus.FINISHED))

    view = ViewModel(items,User())

    assert  len(view.todo_items) == 0
    assert  len(view.finished_items) == 1
    assert  len(view.doing_items) == 0 
    assert view.has_todo_items == False
    assert view.has_doing_items == False
    assert view.has_finished_items == True

def test_NoItems():
    items = []
    view = ViewModel(items,User())

    assert  len(view.todo_items) == 0
    assert  len(view.finished_items) == 0
    assert  len(view.doing_items) == 0 
    assert view.has_todo_items == False
    assert view.has_doing_items == False
    assert view.has_finished_items == False