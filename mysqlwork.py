"""
Created on March 2015
@author: ma56nin / Matt
Contact: ma56nin@hotmail.com
"""

try:
    import pyodbc
except ImportError:
    print("pyodbc python module not able to import")
    exit()

import config
import datetime

driver = config.driver
host = config.host
user = config.user
password = config.password
dbname = config.dbname

# try:
#     import MySQLdb
# except ImportError:
#     print("MySQLdb python module not able to import")
#     exit()
#
# def _connect():
#     db = MySQLdb.connect(host, user, password, dbname)
#     cursor = db.cursor()
#     return db, cursor

def _connect():
    """
    connect to database
    :return:
        db: pyodbc db object of connected database
        cursor: pyodbc cursor object of connected database
    """

    db = pyodbc.connect("Driver={%s};SERVER=%s;DATABSE=%s;UID=%s;PWD=%s;"
                        % (driver, host, dbname, user, password))
    cursor = db.cursor()
    return db, cursor


def add_records(table, report):
    """
    This process updates the database table appropriately
    :param table: string - name of the table to update
    :param report: [userID, IGN, verdict, mod, channel, link="Null"
        userID: string - Slack ID of the user who reported
        IGN: string - Ban, Clean or Indeterminate
        verdict: string - BanCount or CleanCount
        mod: string - ID of the mod who banned
        channel: string - ID of the channel the report is in
        link="NULL": link to video (if applicable)
    """
    db, cursor = _connect()

    userId, ign, verdict, mod, channel, link = (i for i in report)
    sqlcode = "INSERT INTO %s (UserID, IGN, Verdict, ModID, Channel, Link) " \
              "VALUES ('%s', '%s','%s', '%s', '%s', '%s');" \
              % (table, userId, ign, verdict, mod, channel, link)

    db.execute(sqlcode)

    db.commit()
    db.close()


def retrieve_values(table, value, cat, time_frame=-1):
    """
    This is used for activity tracking on players and mods
    :param table: string - table to retrieve values from
    :param value: string - UserID or ModID
    :param cat: string - category to retrieve the values from
    :param time_frame: integer - number of days prior
    :return:
        count: amount of times reported/verdicts given
        act_list: list of the activity of the mod
    """

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


def remove_row(ign, table=config.table):
    """
    This is used to remove a row if there is a false verdict or other similar reason
    :param ign: string - the IGN of the hacker of the report to be removed
    :param table: string - table to remove the value from
    :return: success: Boolean - returns True if report found (and removed), False if not
    """

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