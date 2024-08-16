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

        # SQL queries to create tables
        sql = """
        CREATE TABLE IF NOT EXISTS commands (
            id Integer PRIMARY KEY,
            url text,
            datewanted text,
            timewanted text,
            hoursba Integer,
            seats Integer,
            reservation text,
            rundate text,
            runtime text,
            runnow text,
            account text,
            nonstop text,
            duration Integer,
            proxy text,
            retry Integer,
            minidle Integer,
            maxidle Integer
        )
        """
        # cursor executions
        self.cur.execute(sql)
        self.con.commit()

    def reservationValues(self):
        file = open("reservationlist.json", "r")
        listvalue = json.load(file)
        tmplist = [value for value in listvalue]
        tmplist.append("<Not Set>")
        setlist = set(tmplist)
        return sorted(list(setlist), key=str.casefold)

    def proxyValues(self):
        file = open("proxylist.json", "r")
        listvalue = json.load(file)
        tmplist = [value['profilename'] for value in listvalue]
        tmplist.append("<Not Set>")
        setlist = set(tmplist)
        return sorted(list(setlist), key=str.casefold)
    
    def profileValues(self):
        file = open("profilelist.json", "r")
        self.profilelist = json.load(file)
        return [value['email'] for value in self.profilelist]

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
