import subprocess
import os
import json
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

try:
    subprocess.check_output(["pip", "--version"])
    subprocess.call(["pip", "install", "--upgrade", "pip"])
except:
    command  = """curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"""
    #run command
    subprocess.call(command, shell=True)
    #install pip
    subprocess.call(["python", "get-pip.py"])
    #remove get-pip.py
    os.remove("get-pip.py")
    #update pip
    subprocess.call(["pip", "install", "--upgrade", "pip"])

#install requirements
subprocess.call(["pip", "install", "-r", "requirements.txt"])

#Generate ui to py to get images in GUI
commands = [
    ["pyuic6", "-x", "Modules/Account/Account.ui", "-o", "Modules/Account/Account.py"],
    ["pyuic6", "-x", "Modules/Category/Category.ui", "-o", "Modules/Category/Category.py"],
    ["pyuic6", "-x", "Modules/Home/Home.ui", "-o", "Modules/Home/Home.py"],
    ["pyuic6", "-x", "Modules/Login/Sign_in.ui", "-o", "Modules/Login/Sign_in.py"],
    ["pyuic6", "-x", "Modules/Transaction/Transaction.ui", "-o", "Modules/Transaction/Transaction.py"]]
processes = [subprocess.Popen(cmd) for cmd in commands]

# Đợi tất cả các tiến trình chạy xong
for p in processes:
    p.wait()

#prepare for database
load_dotenv(find_dotenv())
host = os.getenv("HOSTNAME")
client = MongoClient(host)

#check there was database named Group11 in client
if "Group11" in client.list_database_names():
    print("Database already existed")
    db = client['Group11']
else:
    #create database
    db = client['Group11']
    print("Database created")
