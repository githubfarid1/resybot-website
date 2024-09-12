import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from os.path import exists
# from settings import *
from dbclass import Account, Multiproxy, ReservationType, BotCheck, BotCheckRun
from sys import platform
from subprocess import Popen, check_call, call
if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE
from dotenv import load_dotenv
import sqlite3
from os.path import dirname, abspath, join

BASE_DIR = dirname(dirname(abspath(__file__)))
load_dotenv(f"{BASE_DIR}/.env")

# breakpoint()
engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(os.getenv('DB_USERNAME'), os.getenv('DB_PASS'), os.getenv('DB_PORT'), os.getenv('DB_NAME')) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()
PYLOC = os.getenv('PYTHON_PATH')
PIPLOC = os.getenv('PIP_PATH')

def export():
    con = sqlite3.connect(os.getenv('BASE_FOLDER') + "db.sqlite3")
    cur = con.cursor()
    cur.row_factory = sqlite3.Row
    if session.query(ReservationType).count() == 0:
        cur.execute("SELECT * FROM botui_reservationtype order by name")
        rows = cur.fetchall()
        for row in rows:
            data = ReservationType(name=row['name'])
            session.add(data)
        print("reservation Updated")
    if session.query(Account).count() == 0:
        cur.execute("SELECT * FROM botui_account")
        rows = cur.fetchall()
        for row in rows:
            data = Account(email=row['email'], token=row['token'], api_key=row['api_key'], payment_method_id=row['payment_method_id'])
            session.add(data)
        print("account Updated")
    
    if session.query(Multiproxy).count() == 0:
        cur.execute("SELECT * FROM botui_multiproxy")
        rows = cur.fetchall()
        for row in rows:
            data = Multiproxy(name=row['name'], value=row['value'])
            session.add(data)
        print("multiproxy Updated")
    session.flush()        
    session.commit()

def main():
    export()

if __name__ == '__main__':
    main()
