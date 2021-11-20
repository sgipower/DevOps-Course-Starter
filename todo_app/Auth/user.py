from flask_login import UserMixin

writers = [24620559]

class User(UserMixin):
    def __init__(self, id_=123, name = "name", email= "email", profile_pic= "profile_pic"):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.type = type
    def isWriter(self):
        return self.id in writers      

     
