import sqlite3
import os
import sys
import json
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


class Database:
    def __init__(self, db):
        # creating database connection
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def getBotRunById(self, id):
        self.cur.execute("SELECT * FROM botui_botrun WHERE id=?", (id,))
        return self.cur.fetchone()

    def reservationValues(self):
        self.cur.execute("SELECT * FROM botui_reservationtype order name")
        rows = self.cur.fetchall()
        return rows

    def proxyValues(self):
        self.cur.execute("SELECT * FROM botui_proxy order name")
        rows = self.cur.fetchall()
        return rows
    
    def multiProxyValues(self):
        self.cur.execute("SELECT * FROM botui_multiproxy order name")
        rows = self.cur.fetchall()
        return rows

    def accountValues(self):
        self.cur.execute("SELECT * FROM botui_account order email")
        rows = self.cur.fetchall()
        return rows

    def updateAccount(self, email, token, api_key, payment_method_id):
        sql_insert_query = """UPDATE botui_account SET token=?, api_key=?, payment_method_id=? WHERE email=?"""
        self.cur.execute(sql_insert_query, (token, api_key, payment_method_id, email))
        self.con.commit()


    def getCheckBooking(self, id):
        self.cur.execute("SELECT * FROM botui_botcheck where id=?", (id,))
        return self.cur.fetchone()


    def getMultiproxy(self, id):
        self.cur.execute("SELECT * FROM botui_multiproxy where id=?", (id,))
        return self.cur.fetchone()

    def getAccount(self, id):
        self.cur.execute("SELECT * FROM botui_account where id=?", (id,))
        return self.cur.fetchone()

    def getReservation(self, id):
        self.cur.execute("SELECT * FROM botui_reservationtype where id=?", (id,))
        return self.cur.fetchone()

    def getCheckBookingRun(self, id):
        self.cur.execute("SELECT * FROM botui_botcheckrun where id=?", (id,))
        return self.cur.fetchone()

    def getCheckBookingRunAll(self):
        self.cur.execute("SELECT * FROM botui_botcheckrun order by id")
        return self.cur.fetchall()

    def getTaskToRun(self):
        self.cur.execute("SELECT * FROM botui_botcheckrun where task=1 AND pid=0")
        return self.cur.fetchall()

    def getTaskToStop(self):
        self.cur.execute("SELECT * FROM botui_botcheckrun where task=2 AND pid<>-1")
        return self.cur.fetchall()

    def getTaskToDelete(self):
        self.cur.execute("SELECT * FROM botui_botcheckrun where task=3")
        return self.cur.fetchall()

    def updateBotrunPid(self, pid, id):
        sql_query = """UPDATE botui_botcheckrun SET pid=? WHERE id=?"""
        self.cur.execute(sql_query, (pid, id))
        self.con.commit()

    def deleteBotrun(self, id):
        sql_query = """DELETE FROM botui_botcheckrun WHERE id=?"""
        self.cur.execute(sql_query, (id, ))
        self.con.commit()
