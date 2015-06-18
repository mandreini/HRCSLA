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
    This process updates the database table appropriately. userId and name are always length 1 lists
    :param table: string - name of the table to update
    :param report: [userID, IGN, verdict, mod, channel, link="Null"
        userId: list - Slack ID of the user who reported
        name: list - Slack username of the user who reported
        IGN: string - Ban, Clean or Indeterminate
        verdict: string - BanCount or CleanCount
        mod: string - ID of the mod who banned
        channel: string - ID of the channel the report is in
        link="NULL": link to video (if applicable)
    """
    db, cursor = _connect()

    userId, name, ign, verdict, mod, channel, link = (i for i in report)
    sqlcode = "INSERT INTO %s (UserID, Name, IGN, Verdict, ModID, Channel, Link) " \
              "VALUES ('%s', '%s', '%s','%s', '%s', '%s', '%s');" \
              % (table, userId[0], name[0], ign, verdict, mod, channel, link)

    db.execute(sqlcode)

    db.commit()
    db.close()

def check_for_existing_report(report, table=config.table):
    """
    This is used as part of a sequence of checks to prevent duplicate report entries.
    userId and name are always length 1 lists
    :param report: list - report to be checked in the database
    :param table: string - table to check for duplicate
    :return: bool - True if existing report, False otherwise
    """
    db, cursor = _connect()
    userId, name, ign, verdict, mod, channel, link = (i for i in report)
    sqlcode = """SELECT * FROM %s WHERE
                 UserID = '%s' AND
                 Name = '%s' AND
                 IGN = '%s' AND
                 Verdict = '%s' AND
                 Channel = '%s';
                 """ \
                % (table, userId[0], name[0], ign, verdict, channel)

    c = db.execute(sqlcode)
    data = c.fetchall()
    db.commit()
    db.close()  # just to make sure
    return len(data) > 0


def _check_for_duplicates(db, cursor, table=config.table):
    """
    Checks if duplicate records exist in the table
    :param table: string - table to check for duplicate reports in
    :return: True if duplicates are found, False otherwise
    """

    sqlcode = """SELECT UserID, IGN, Verdict, ModID, Channel,
                 Count(*) FROM %s as dupes
                 GROUP BY UserID, IGN, Verdict, ModID, Channel
                 Having COUNT(*) > 1;""" % table

    c = db.execute(sqlcode)
    data = c.fetchall()
    return len(data) > 0


def remove_duplicates(table=config.table):
    """
    This will remove duplicate reports that manage to slip through my net of checks somehow
    sqlcode from http://stackoverflow.com/questions/4685173/delete-all-duplicate-rows-except-for-one-in-mysql
    :param table: string - table to check for duplicate reports
    """

    db, cursor = _connect()
    if _check_for_duplicates(db, cursor, table):
        sqlcode = """
            DELETE FROM %s
              WHERE id NOT IN (
                SELECT * FROM (
                  SELECT MIN(n.id) FROM brawl_records_test n
                  GROUP BY n.UserID, n.IGN, n.Verdict, n.ModID, n.Channel
                ) x
              ); """ % table

        db.execute(sqlcode)
        db.commit()
        db.close()
        cursor.close()

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
    return True


def add_from_file(filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.split('\t')
        line = line[:4] + ['Unknown'] + line[4:-1] + [line[-1].strip('\n')] + ['NULL']
        add_records("hrc_records_test", line)


def retieve_values_id(id, timeframe=-1, table=config.table):
    """
    This function will retrieve all the records associated with id from the table
    :param id: string - id of the user
    :param timeframe: int - amount of days to look back. Default -1 means all time
    :param table: string - table to connect to
    :return: [collection] of records
    """

    db, cursor = _connect()

    # look into porting the if statement to the sql query
    if timeframe != -1:
        sqlcode = """
          SELECT * FROM %s WHERE
            UserID = '%s';
            """ % (table, id)
    else:
        sqlcode = """
            SELECT * FROM %s WHERE
              USERID = '%s' AND
              GETDATE() - Date < %s;
              """ % (table, id, timeframe)

    c = db.execute(sqlcode)
    data = c.fetchall()
    return data


def retrieve_values_name(name, timeframe=-1, table=config.table):
    """
    This function will retrieve all the records associated with the given name from the table.
    Supports change of username
    :param name: string - username of the user
    :param timeframe: int - amount of days to look back. Default -1 means all time
    :param table: string - table to connect to
    :return: [collection] of records
    """

    db, cursor = _connect()

    idcode = """
        SELECT UserID from %s WHERE
          Name = '%s';
          """ % (table, name)
    c1 = db.execute(idcode)
    data = c1.fetchall()
    userid = data  # id = data[0]

    if timeframe != -1:
        sqlcode = """
            SELECT * FROM %s WHERE
              UserID = '%s';
              """ % (table, userid)
    else:
        sqlcode = """
        Select * FROM %s WHERE
          USERID = '%s' AND
          GETDATE() - DATE < %s;
          """ % (table, userid, timeframe)

    c2 = db.execute(sqlcode)
    data = c2.fetchall()
    return data

# add_from_file("reports_record.dat")