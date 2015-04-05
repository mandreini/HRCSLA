"""
Created on March 2015
@author: ma56nin / Matt
Contact: ma56nin@hotmail.com
"""

try:
    import MySQLdb
except ImportError:
    print("MySQLdb python module not able to import")

import config
import datetime

host = config.host
user = config.user
password = config.password
dbname = config.dbname


def _connect():
    db = MySQLdb.connect(host, user, password, dbname)
    cursor = db.cursor()
    return db, cursor

def add_records(table, report):
    # This process updates the database table appropriately
    # inputs:
        # table: string - name of the table to update
        # userID: string - Slack ID of the user who reported
        # IGN: string - Ban, Clean or Indeterminate
        # verdict: string - BanCount or CleanCount
        # mod: string - ID of the mod who banned
        # channel: string - ID of the channel the report is in
        # link="NULL": link to video (if applicable)

    db, cursor = _connect()

    userId, ign, verdict, mod, channel, link = (i for i in report)

    db.execute("INSERT INTO %s (UserID, IGN, Verdict, ModID, Channel, Date, Link)" +
               "VALUES ('%s', '%s', '%s','%s', '%s', ''%s', 'SELECT CURDATE()', %s');"
               % (table, userId, ign, verdict, channel, mod, link))

    db.commit()
    db.close()
    cursor.close()

def retrieve_values(table, value, cat, time_frame=-1):
    # This is used for activity tracking on players and mods
    # inputs:
        # table: string - table to retrieve values from
        # value: string - UserID or ModID
        # time_frame: integer - number of days prior
    # outputs:
        # count: amount of times reported/verdicts given
        # act_list: list of the activity of the mod

    # db.execute("SELECT %s FROM %s WHERE DATEDIFF(CURDATE(), Date) <= %s;" % (value, table, time_frame))

    # pull all activity of a player
    db, cursor = _connect()
    act_list = []

    db.execute("SELECT * FROM %s WHERE %s = %s;" % (table, cat, value))
    data = db.fetchall()
    if time_frame == -1:
        act_list = data
    else:
        for row in data:
            cdate = datetime.datetime.now()
            repdate = datetime.datetime.strptime(row[5], "%Y-%m-%d")
            ddif = cdate - repdate
            ddif = ddif.days

            if ddif <= time_frame:
                act_list.append(row)

    count = len(act_list)

    # Potential alternative:
    # db.execute("SELECT * FROM %s WHERE %s = %s;" % (table, cat, value))
    # db.execute("SELECT * FROM %s WHERE CURDATE() - date < %s;" %s table)
    # data = cursor.fetchall()

    db.close()
    cursor.close()

    return count, act_list

def remove_row(ign):
    # This is used to remove a row if there is a false verdict or other similar reason
    # inputs:
        # IGN: string - the IGN of the hacker of the report to be removed
    # outputs:
        # success: Boolean - returns True if report found (and removed), False if not

    db, cursor = _connect()

    db.execute("SELECT id FROM %s WHERE IGN = %s;" % (table, ign))
    data = db.fetchall()
    if len(data) == 0:
        return False

    db.execute("DELETE FROM %s WHERE IGN = %s LIMIT 1;" % (table, ign))
    db.commit()
    db.close()
    cursor.close()
    return True