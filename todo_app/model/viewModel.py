from todo_app.data.itemstatus import ItemStatus

class ViewModel:
    def __init__(self, items,user_):
        self._items = items
        self.userID = user_.id
        self.userName = user_.name
        self.avatar = user_.profile_pic
        self.userIsWriter = user_.isWriter()
    @property
    def has_todo_items(self):
        res = next((item for item in self._items if item.status == ItemStatus.TODO), None)
        return res != None 
    @property
    def has_doing_items(self):
        res = next((item for item in self._items if item.status == ItemStatus.DOING), None)
        return res != None 
    @property
    def has_finished_items(self):
        res = next((item for item in self._items if item.status == ItemStatus.FINISHED), None)
        return res != None            
    @property
    def todo_items(self):
        return [item for item in self._items if item.status == ItemStatus.TODO]
    @property
    def doing_items(self):
        return [item for item in self._items if item.status == ItemStatus.DOING]
    @property
    def finished_items(self):
        return [item for item in self._items if item.status == ItemStatus.FINISHED]