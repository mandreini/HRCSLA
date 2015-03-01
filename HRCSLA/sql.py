"""
Created on July, 2014
@author: ma56nin9 / Matt
Contact: ma56nin@hotmail.com
"""

import sqlite3
import web

def close_table(table):
    conn = sqlite3.connect("HRC_records.db")
    conn.execute("DROP TABLE " + table + ";")
    conn.close()
    return
    
def create_table(table):   
    conn = sqlite3.connect("HRC_records.db")
    conn.execute('CREATE TABLE ' + table + '''
        (id integer primary key,
         Reporter text,
         Ban integer,
         Clean integer,
         Accuracy text,
         Total integer,
         created timestamp DEFAULT current_timestamp);''')
    
    db.insert(table,Reporter=table,Ban=0,Clean=0,Accuracy="0.0",Total=0) #to title the webpage
    conn.close()
    return

def try_table(table):
    try:
        create_table(table)
    except sqlite3.OperationalError:
        print "Refreshing table"
        close_table(table)
        create_table(table)
        
tables = ["all_time", "last_month", "this_week", "today"]
render = web.template.render('templates/',base='base')
db = web.database(dbn='sqlite', db='HRC_records.db')