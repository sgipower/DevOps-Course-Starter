from flask_login import UserMixin

writers = [24620559]

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic,type):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.type = type
    def __init__(self):
        self.id=123
        self.name = "name"
        self.email = "email"
        self.profile_pic = "profile_pic"
        self.type = "type"
    def isWriter(self):
        return self.id in writers      

     
