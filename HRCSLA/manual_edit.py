"""
Created on July, 2014
@author: ma56nin9 / Matt
Contact: ma56nin@hotmail.com
"""

import sys
import sqlite3
import sql

def open_reports():
    try:
        f = open("reports_record.dat","r")
    except:
        print("File 'reports_record.dat' not found. \nAdd the reports from the HRCLM exported to notepad, then run again.")
        f = open("reports_record.dat","w")
        f.close()
        sys.exit()
    
    report_list = f.readlines()[1:]
    
    for i in range(len(report_list)):
        report_list[i] = report_list[i].strip("\n")
        report_list[i] = report_list[i].split("\t")
        report_list[i][3] = report_list[i][3].split("-")
        for d in range(3):
            if report_list[i][3][d][0] == "0": 
                report_list[i][3][d] = report_list[i][3][d][1:]
            if d == 2:
                if len(report_list[i][3][d]) == 2:
                    report_list[i][3][d] = "20" + report_list[i][3][d]
            report_list[i][3][d] = int(report_list[i][3][d])
        report_list[i][3][0],report_list[i][3][2] = report_list[i][3][2],report_list[i][3][0]
    return report_list
        
def _get_names(HRC_list):
    return [i[:3] for i in HRC_list]

def _get_dates(HRC_list):
    date_list = [HRC_list[i][3] for i in range(len(HRC_list))]
    for j in range(len(date_list)):
        for k in range(3):
            date_list[j][k] = str(date_list[j][k])
    date_list = ["/".join(date) for date in date_list]
    return date_list

def _clear_records():
    open("reports_record.dat","w")
    
def add_report(rep,IGN,verdict,table):
    conn = sqlite3.connect("HRC_records.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM " + table + " WHERE Reporter = ?",(rep,))
    data = cursor.fetchall()
    if len(data) == 0: #if the reporter is not in the database, add him
        sql.db.insert(table,Reporter=rep,Ban=0,Clean=0,Accuracy="0.0",Total=0)
        
    conn.execute("UPDATE " + table + " SET " + verdict + " = " + verdict + " + 1 WHERE Reporter = '" + rep + "';")
    conn.commit()
    conn.close()

def indiv_report():
    try:
        v = open("reports_to_add.txt",'r')
    except:
        print("'reports_to_add.txt' not found. Please do not remove the file, only edit it! A new one will be automatically created")
        v = open("reports_to_add.txt",'w') #refresh file, v.truncate() isn't working?
        v.write("#This file is for manually adding a report to the system.\n#The report structure is as follows:\n#Reporter IGN verdict day-month-year ; mind the spacing and hyphens! Use numbers for date only")
        return 0
        
    new_indiv = v.readlines()[3:]
    
    if v: #v exists, is not emtpy/null from only 4 lines of the file i.e. nothing to add
        v = open("reports_to_add.txt",'w') #refresh file, v.truncate() isn't working?
        v.write("#This file is for manually adding a report to the system.\n#The report structure is as follows:\n#Reporter IGN verdict day-month-year ; mind the spacing and hyphens! Use numbers for date only")

    return new_indiv