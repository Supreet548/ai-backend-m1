class UserHelper:
    def __init__(self,name):
        self.name =name

    def welcome(self):
        return f"Welcome {self.name}"
    
    def role(self):
        return "Backend Learner"