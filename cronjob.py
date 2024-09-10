import schedule
import time
from botmodules.database import Database
import psutil
import os
from sys import platform
from dotenv import load_dotenv
from subprocess import Popen, check_call, call
if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE

load_dotenv()
PYTHON_EXE = os.getcwd() + os.sep + r"venv\Scripts\python.exe"
if platform == "linux" or platform == "linux2":
    PYLOC = os.getenv('PYTHON_PATH')
    PIPLOC = os.getenv('PIP_PATH')
elif platform == "win32":
    PYLOC = PYTHON_EXE
    PIPLOC = os.getcwd() + os.sep + r"venv\Scripts\pip.exe"

db = Database("db.sqlite3")

def updatepidstatus():
    for data in db.getCheckBookingRunAll():
        pid = data['pid']
        id = data['id']
        if pid !=0 and psutil.pid_exists(pid):
            if psutil.Process(pid).status() == 'zombie':
                db.updateBotrunPid(id=id, pid=-1)                
        if pid !=0 and not psutil.pid_exists(pid):
            db.updateBotrunPid(id=id, pid=-1)

def runcheckbooking():
    for data in db.getTaskToRun():
        print("run")
        fname = open(f"logs/checkbookrun_web_{data[0]}.log", "w")
        commandlist = [PYLOC, "botmodules/resybotcheckbooking.py", "-id", '{}'.format(data[0]) ]
        process = Popen(commandlist, stdout=fname)
        # print(" ".join(commandlist))
        db.updateBotrunPid(id=data[0], pid=process.pid)

def stopcheckbooking():
    for data in db.getTaskToStop():
        print("stop")
        pid = data['pid']
        id = data['id']
        try:
            proc = psutil.Process(int(pid))
            proc.terminate()
        except:
            pass
        db.updateBotrunPid(id=id, pid=-1)


def delcheckbooking():
    for data in db.getTaskToDelete():
        print("del")
        pid = data['pid']
        id = data['id']
        try:
            proc = psutil.Process(int(pid))
            proc.terminate()
        except:
            pass
        time.sleep(0.5)        
        try:
            os.remove(f"logs/checkbookrun_web_{id}.log")
        except:
            pass
        db.deleteBotrun(id)

# delcheckbooking()
# runcheckbooking()

schedule.every(5).seconds.do(runcheckbooking)
schedule.every(10).seconds.do(stopcheckbooking)
schedule.every(10).seconds.do(delcheckbooking)
schedule.every(60).seconds.do(updatepidstatus)

while True:
    schedule.run_pending()