from traceback import TracebackException

from Api.MainAPI import API

class SignupAPI(API):
    def __init__(self):
        super().__init__()
        self.connector()

    def check_user_signup(self, username, password, repassword ):
        try:
            if username == '' or password == '' or repassword == '':
                return 1 #Error 1: Username or password is empty
            if password != repassword:
                return 2 #Error 2: Password is not the same
             #Not found = None
            user = self.users_collection.find_one({'username': username})
            if user != None:
                return 3 #Error 3: Username is already exist

            self.users_collection.insert_one({'username': username, 'password': password})
            return 0 #Success in register
        except Exception as e:
            print(e)
            return str(e)