from todo_app.data.itemstatus import ItemStatus

class Item:
    def __init__(self,id = None,status=None,title=None):
        self.id= id if id is not None else -1
        self.status= status if status is not None else ItemStatus.TODO
        self.title= title if title is not None else 'List saved todo items'
        self.cardid= id
    def unstarted(self):
        return self.status == ItemStatus.TODO
    def started(self):
        return self.status == ItemStatus.DOING
    def finished(self):
        return self.status == ItemStatus.FINISHED                
    def description(self):
        return ItemStatus(self.status).name  
    def __str__(self):
     return "id:" + str(self.id)  
