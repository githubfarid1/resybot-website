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


    def reservationValues(self):
        self.cur.execute("SELECT * FROM botui_reservationtype order name")
        rows = self.cur.fetchall()
        return rows

    def proxyValues(self):
        self.cur.execute("SELECT * FROM botui_proxy order name")
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

    # Add Instructor record to the table
    def insertCommand(self, url, datewanted, timewanted, hoursba, seats, reservation, rundate, runtime, runnow, account, nonstop, duration, proxy, retry, minidle, maxidle):
        self.cur.execute("INSERT INTO commands VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (url, datewanted, timewanted, hoursba, seats, reservation, rundate, runtime, runnow, account, nonstop, duration, proxy, retry, minidle, maxidle))
        self.con.commit()


    # Display Instructor List from table
    def viewCommand(self):
        self.cur.execute("SELECT * FROM commands order by id desc")
        rows = self.cur.fetchall()
        dlist = []
        for row in rows:
            rowlist = list(row)
            rowlist.append(rowlist[1]) 
            rowlist[1] = rowlist[1].split("/")[-1]
            dlist.append(tuple(rowlist))
        return dlist

    # Delete Instructor Entry from table
    def removeCommand(self, comid):
        self.cur.execute("DELETE FROM commands WHERE id=?", (comid,))
        self.con.commit()

    # Edit Instructor Details in the table
    def updateCommand(self, comid, url, datewanted, timewanted, hoursba, seats, reservation, rundate, runtime, runnow, account, nonstop, duration, proxy, retry, minidle, maxidle):
        sql_insert_query = """UPDATE commands SET url=?, datewanted=?, timewanted=?, hoursba=?, seats=?, reservation=?, rundate=?, runtime=?, runnow=?, account=?, nonstop=?, duration=?, proxy=?, retry=?, minidle=?, maxidle=? WHERE id=?"""
        self.cur.execute(sql_insert_query, (url, datewanted, timewanted, hoursba, seats, reservation, rundate, runtime, runnow, account, nonstop, duration, proxy, retry, minidle, maxidle, comid))
        self.con.commit()
