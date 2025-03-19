from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

class API:
    def __init__(self):
        self.connector()

    def connector(self): #connect tới localhost MongoDB
        load_dotenv(find_dotenv())
        host = os.getenv("HOSTNAME") #truy xuất giá trị của biến môi trường HOSTNAME
        self.client = MongoClient(host)
        self.db = self.client['Group11']
        self.users_collection = self.db['users']
        self.expenses_collection = self.db['expenses']

    def get_users_data(self):
        users_data = list(i for i in self.users_collection.find()) #trả về đường dẫn <>
        return users_data

    def get_expenses_data(self):
        accounts = self.expenses_collection.find()  # trả về đường dẫn connect <>
        expenses_data = []
        for account in accounts:
            if 'Username1' in account:
                for item in account['Username1']: #Thay thành biến tên user đang dùng app
                    temp={}
                    temp["Categories"]=item["Categories"]
                    temp["Details"]=item["Details"]
                    temp["Amount"]=item["Amount"]
                    temp["Date"]=item["Date"]
                    expenses_data.append(temp)
        return expenses_data

# a=API()
# print(list(a.get_expenses_data()))
