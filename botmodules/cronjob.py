import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from os.path import exists
# from settings import *
from dbclass import BotCheckRun
import psutil
from sys import platform
from subprocess import Popen, check_call, call
if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE
from dotenv import load_dotenv
import time
import schedule
from os.path import dirname, abspath, join

BASE_DIR = dirname(dirname(abspath(__file__)))
load_dotenv(f"{BASE_DIR}/.env")
engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(os.getenv('DB_USERNAME'), os.getenv('DB_PASS'), os.getenv('DB_PORT'), os.getenv('DB_NAME')) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()
PYLOC = os.getenv('PYTHON_PATH')
PIPLOC = os.getenv('PIP_PATH')
RESY_API_KEY='VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5'

def updatepidstatus():
    for data in session.query(BotCheckRun).all():
        pid = data.pid
        id = data.id
        if pid !=0 and psutil.pid_exists(pid):
            if psutil.Process(pid).status() == 'zombie':
                session.query(BotCheckRun).filter(BotCheckRun.id==id).update({"pid":-1})
        if pid !=0 and not psutil.pid_exists(pid):
            session.query(BotCheckRun).filter(BotCheckRun.id==id).update({"pid":-1})
    session.flush()
    session.commit()

def runcheckbooking():
    for data in session.query(BotCheckRun).filter(BotCheckRun.task==1, BotCheckRun.pid==0).all():
        print("run")
        id = data.id
        fname = open(f"{os.getenv('BASE_FOLDER')}logs/checkbookrun_web_{id}.log", "w")
        commandlist = [PYLOC, f"{os.getenv('BASE_FOLDER')}botmodules/resybotcheckbooking.py", "-id", '{}'.format(id), "-apikey", '{}'.format(RESY_API_KEY) ]
        process = Popen(commandlist, stdout=fname)
        session.query(BotCheckRun).filter(BotCheckRun.id==id).update({"pid":process.pid})
    session.flush()
    session.commit()

def stopcheckbooking():
    for data in session.query(BotCheckRun).filter(BotCheckRun.task == 2, BotCheckRun.pid != -1).all():
        print("stop")
        pid = data.pid
        id = data.id
        try:
            proc = psutil.Process(int(pid))
            proc.terminate()
        except:
            pass
        session.query(BotCheckRun).filter(BotCheckRun.id==id).update({"pid":-1})
    session.flush()
    session.commit()


def delcheckbooking():
    for data in session.query(BotCheckRun).filter(BotCheckRun.task == 3).all():
        print("del")
        pid = data.pid
        id = data.id
        try:
            proc = psutil.Process(int(pid))
            proc.terminate()
        except:
            pass
        time.sleep(0.5)        
        try:
            os.remove(f"{os.getenv('BASE_FOLDER')}logs/checkbookrun_web_{id}.log")
        except:
            pass
        # db.deleteBotrun(id)
        session.query(BotCheckRun).filter(BotCheckRun.id==id).delete()
    session.flush()
    session.commit()


def main():
    schedule.every(5).seconds.do(runcheckbooking)
    schedule.every(10).seconds.do(stopcheckbooking)
    schedule.every(10).seconds.do(delcheckbooking)
    schedule.every(60).seconds.do(updatepidstatus)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main()
