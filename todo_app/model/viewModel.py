from todo_app.data.itemstatus import ItemStatus

class ViewModel:
    def __init__(self, items):
        self._items = items
    @property
    def has_todo_items(self):
        res = next((item for item in self._items if item.status == ItemStatus.TODO), None)
        if res == None:
            return False
        else:
            return True
    @property
    def has_doing_items(self):
        res = next((item for item in self._items if item.status == ItemStatus.DOING), None)
        print(res)
        if res == None:
            return False
        else:
            return True
    @property
    def has_finished_items(self):
        res = next((item for item in self._items if item.status == ItemStatus.FINISHED), None)
        if res == None:
            return False
        else:
            return True            
    @property
    def todo_items(self):
        return (item for item in self._items if item.status == ItemStatus.TODO)
    @property
    def doing_items(self):
        return (item for item in self._items if item.status == ItemStatus.DOING)
    @property
    def finished_items(self):
        return (item for item in self._items if item.status == ItemStatus.FINISHED)