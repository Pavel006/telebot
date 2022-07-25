#import sqlite3

TOKEN = "1060305984:AAF_XAXey0817qcI95VRSWdvfPbQze29Q2Y"
APP_URL = " https://kazinobot221.herokuapp.com/" + TOKEN

__connection = None

def get_connection():
    global  __connection
    if __connection is None:
        __connection = sqlite3.connect('database/database.db')
        return __connection