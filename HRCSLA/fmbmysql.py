"""
Created on March 2015
@author: ma56nin / Matt
Contact: ma56nin@hotmail.com
"""

import MySQLdb

host     = "vweb20.nitrado.net"
user     = "ni78781_3sql4"
password = "295b4e12"
dbname   = "ni78781_3sql4"
table    = "sample_hrc_data"

def connect():
    conn = MySQLdb.Connection(user=user, passwd=password, host=host, db=dbname)
    cursor = conn.cursor()
    return conn, cursor

def retrieve_info():
    cursor.execute("SELECT * FROM %s" % table)
    fields = cursor.fetchall()
    my_fields = [field for field in fields]
    return my_fields
        
def insert_data(report):
    #report: [<reporter>, <IGN>, <verdict>, <date in [yyyy,mm,dd]>, <mod-who-banned>]

conn, cursor = connect()    
cursor.close()
conn.close()

