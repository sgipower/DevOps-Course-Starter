from todo_app.data import itemstatus
from todo_app.data.itemstatus import ItemStatus
from todo_app.model.viewModel import ViewModel
from todo_app.data.item import Item

def test_CheckTodoList():
    items = []
    items.append(Item(1,ItemStatus.TODO))

    view = ViewModel(items)

    assert  sum(1 for _ in view.todo_items) == 1 
    assert  sum(1 for _ in view.finished_items) == 0
    assert  sum(1 for _ in view.doing_items) == 0 
    assert view.has_todo_items == True
    assert view.has_doing_items == False
    assert view.has_finished_items == False

def test_CheckDoingList():
    items = []
    items.append(Item(1,ItemStatus.DOING))

    view = ViewModel(items)

    assert  sum(1 for _ in view.todo_items) == 0 
    assert  sum(1 for _ in view.finished_items) == 0
    assert  sum(1 for _ in view.doing_items) == 1
    assert view.has_todo_items == False
    assert view.has_doing_items == True
    assert view.has_finished_items == False

def test_CheckDoneList():
    items = []
    items.append(Item(1,ItemStatus.FINISHED))

    view = ViewModel(items)

    assert  sum(1 for _ in view.todo_items) == 0
    assert  sum(1 for _ in view.finished_items) == 1
    assert  sum(1 for _ in view.doing_items) == 0 
    assert view.has_todo_items == False
    assert view.has_doing_items == False
    assert view.has_finished_items == True

def test_NoItems():
    items = []
    view = ViewModel(items)

    assert  sum(1 for _ in view.todo_items) == 0
    assert  sum(1 for _ in view.finished_items) == 0
    assert  sum(1 for _ in view.doing_items) == 0 
    assert view.has_todo_items == False
    assert view.has_doing_items == False
    assert view.has_finished_items == False