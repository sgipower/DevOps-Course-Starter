from flask_login import UserMixin
writers = [24620559,0]

class User(UserMixin):
    def __init__(self, id_=0, name = "name", email= "email", profile_pic= "https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50"):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.type = type
    def isWriter(self):
        return self.id in writers      

     
