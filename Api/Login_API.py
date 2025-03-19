from Api.MainAPI import API

class LoginAPI(API):
    def __init__(self):
        super().__init__()  
        self.connector()
        
    def check_user_login(self,username,password):
        if username == '' or password == '':
            return 1 #Error 1:Username or password is empty
        user=self.users_collection.find_one({'username':username})
        if user == None:
            return 2 #Error 2: User not found
        if user["password"] != password or user["username"] != username:
            return 3 #Error 3: Incorrect Username or Password
        return user["username"] #trả về tên user để access cho đúng tài khoản user
