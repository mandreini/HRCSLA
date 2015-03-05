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

def _connect():
    db = MySQLdb.connect(host, user, password, dbname)
    cursor = db.cursor()
    return db, cursor
    
def _close():
    cursor.close()
    db.close()

def _retrieve_info(table):
    cursor.execute("SELECT * FROM %s" % table)
    fields = cursor.fetchall()
    my_fields = [field for field in fields]
    return my_fields
        
def update(userId, verdict, record, rep_name, table):
    #report: [<reporter>, <IGN>, <verdict>, <date in [yyyy,mm,dd]>, <mod-who-banned>]
    #record: [<ban count>, <clean count>]

    db, cursor = _connect()
    if verdict == "clean":
        verdict = "CleanCount"
    elif verdict == "ban":
        verdict = "BanCount"

    cursor.execute("SELECT id FROM %s WHERE UserID = '%s';" % (table, userId))
    data = cursor.fetchall()
    if len(data) == 0: #if the reporter is not in the database, add him.
        cursor.execute("INSERT INTO sample_hrc_data(UserID, Name, BanCount, \
          CleanCount, Accuracy, Total) VALUES ('%s', '%s', '%d', '%d', '%s', '%d');" 
          % (user, rep_name, 0, 0, '0', 0))
    cursor.execute("UPDATE %s SET %s = %s + 1 WHERE UserID = '%s'" 
    % (table, verdict, verdict, user))
    
    if record[0] == 0 and record[1] == 0:
        new_acc = 0.
    else:
        new_acc = int((float(record[0]) / float(record[0] + record[1]))*100.)
        
    cursor.execute("UPDATE %s SET Accuracy = %s WHERE UserID = '%s';" % (table, str(new_acc), userId))
    cursor.execute("UPDATE %s SET TOTAL = TOTAL + 1 WHERE UserID = '%s';" % (table, userId))
    
    cursor.execute("SELECT Name from %s WHERE UserID = '%s';" % (table, userId))
    oldName = cursor.fetchall()
    oldName = oldName[0][0]
    if oldName != rep_name:
        cursor.execute("UPDATE %s SET Name = '%s' WHERE UserID = '%s';" % (table, rep_name, userId))
    
    db.commit()
    _close()    

#debug stuffs
db, cursor = _connect()
psuedo_users = {"U1234": "ma56nin", "U42": "jacobcrofts", "U72": "HoboHunt3r", "U1234": "ma56nin9"}
r1 = ["U1234", "AceBlue", "ban", [2015,3,4], "wizard0817"]
r2 = ["U1234", "Bubbly", "ban", [2015,3,4], "Xxenon"]
r3 = ["U72", "Vendrick", "ban", [2015,3,4], "Throttlezz"]
r4 = ["U42", "hclewk", "ban", [2015,3,4], "ma56nin"]
