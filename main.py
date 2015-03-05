"""
Created on July, 2014
@author: ma56nin / Matt
Contact: ma56nin@hotmail.com
"""

try:
    import customization
    import sql
    import manual_edit
    import features
    import fmbmysql
    import SlackBot
except:
    print("customization, sql, manual_edit, features or SlackBot not able to import.")
    exit

try:
    import sqlite3    
    import time   
    import datetime
except:
    print("sqlite3, time and datetime modules of python were unable to import, check python installation.")
    exit
            
def start_log(): #infinite loop, runs main() every minute
    t = time.gmtime()
    while True:
        if time.gmtime()[1] != t[1]:
            pass
            #refresh month database
            #update player/mod activity log
        if time.gmtime()[3] != t[3]:
            pass
            #refresh week database
        if time.gmtime()[2] != t[2]:
            pass
            #refresh day database
        if time.gmtime()[4] != t[4]:
            add_new_reports(manual_edit.indiv_report())
            bans, cleans = customization.open_files()
            main()
            t = time.gmtime()


def add_new_reports(new_reports):
    #input: list of strings directly inputted ("Reporter IGN verdict day-month-year")
    for n in new_reports:
        try:
            n = n.strip("\n")
            n = n.strip(" ")
            today = datetime.datetime.today()
            date = [today.year, today.month, today.day]
            new_rep = n.split(" ")
            new_rep += [date, "Unknown"]
            write_report(new_rep)
            determine_dict(new_rep)
            print("Report added successfully!")            
        except:
            print("The report '" + n + "' was not compatible. Please recheck the syntaxing")         
            
def main():
    HRCBot.get_new_messages()
    new_reports = HRCBot.new_reports
    for new_report in new_reports:
        write_report(new_report)
        determine_dict(new_report)
            
def write_report(report): #allows you to start the process, then terminate and restart it (i.e. update) without anything (or much)
    #input report: [<reporter>, <IGN>, <verdict>, <date in [yyyy,mm,dd]>, <mod-who-banned>]
#    print "writing report"
    my_reports.append(report)
    b = open("reports_record.dat","r+")
    b.readlines()
    b.write('\n'+str(report[0])+"\t"+str(report[1])+"\t"+str(report[2])+"\t"+str(report[3][2])+"-"+str(report[3][1])+"-"+str(report[3][0])+"\t"+report[4])
    b.close()

def determine_dict(report):
#    print "determining dictionary"
    #same as write_report()'s
    add_to_dict(all_time_reports,report)
    ddif = (datetime.date(report[3][0],report[3][1],report[3][2]) - datetime.date.today()).days
    if ddif < 0:
        ddif *= -1 #idk why it does that...
    if ddif == 0:
        add_to_dict(current_day_reports,report)
    if ddif <= 7:
        add_to_dict(this_week_reports,report)
    if ddif <= 30:
        add_to_dict(last_month_reports,report)
        
def add_to_dict(dictionary,report):
    #inputs: dictionary - which dictionary to add, find out report
#    print("Adding to dictionary for SQLite3 database")
    if not dictionary.has_key(report[0]):
        dictionary[report[0]] = [0,0,0]
    dictionary[report[0]][2] += 1
    if report[2].find("autobanned") != -1:
        pass #don't confuse autoban with ban!
    else:
        for ban in bans:
            if report[2].find(ban) != -1:
                dictionary[report[0]][0] += 1
                update_database(dictionary,report[0],"Ban")          
        for clean in cleans:
            if report[2].find(clean) != -1:
                dictionary[report[0]][1] += 1
                update_database(dictionary,report[0],"Clean")
                
def update_database(table_dict, user, verdict): #add the report to the database
    #table_dict: which database to update, string, string
    if table_dict["name"] == sql.tables[0]: #to allow for different tables
        table = sql.tables[0]
    elif table_dict["name"] == sql.tables[1]:
        table = sql.tables[1]
    elif table_dict["name"] == sql.tables[2]:
        table = sql.tables[2]
    elif table_dict["name"] == sql.tables[3]:
        table = sql.tables[3]
    #table = table_dict['name']
        
    rep_name = HRCBot.user_id_name_database[user]
    conn = sqlite3.connect("HRC_records.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM %s WHERE user = '%s';" % (table, user))
    data = cursor.fetchall()
    if len(data) == 0: #if the reporter is not in the database, add him.
        sql.db.insert(table, user=user, Reporter=rep_name, Ban=0, Clean=0, Accuracy="0.0", Total=0)
        
    conn.execute("UPDATE %s SET %s = %s + 1 WHERE user = '%s';" % (table, verdict, verdict, user))
    conn.execute("UPDATE %s SET Total = Total + 1 WHERE user = '%s';" % (table, user))
    
    if table_dict[rep_name][0] == 0 and table_dict[rep_name][1] == 0:
        new_acc = 0.
    else:
        new_acc = int((float(table_dict[rep_name][0]) / float(table_dict[rep_name][0] + table_dict[rep_name][1]))*100.)
    conn.execute("UPDATE " + table + " SET Accuracy = " + str(new_acc) + " WHERE user = '" + user + "';")
    conn.execute("UPDATE %s SET Accuracy = %s WHERE user = '%s';" % (table, str(new_acc), user))
    
    conn.execute("SELECT Reporter from %s WHERE user = '%s';" % (table, user))   
    data = conn.fetchall()[0][0]
    if data != rep_name:
        conn.execute("UPDATE %s SET Reporter = %s WHERE user = '%s';" % (table, rep_name))
        #note, prone to SQL injection!
        
    conn.commit()
    conn.close()    
    fmbmysql.update(user, verdict, [table_dict[rep_name][0], table_dict[rep_name][1]], rep_name, table)
    #function to update fmb's database in other script

#set up report structure
HRCBot = SlackBot.Bot()
all_time_reports = {"name": sql.tables[0]} #place to store all reports; #records: {Reporter_skype_handle: [bans, clean, reports], ... }; will need to change
last_month_reports = {"name": sql.tables[1]} #same as all_time, but only past 30 days
this_week_reports = {"name": sql.tables[2]} #same as all_time, but only past 7 days
current_day_reports = {"name": sql.tables[3]} #same as all_time, but only today
total_records = [] #[[<reporter>, <IGN>, <verdict>, <mod_who_banned>, [dd,mm,yyy]], ... ]
name_list = [] #to get the id for updating the database
bans, cleans = customization.open_files()

#setup the database
for t in sql.tables:
    sql.try_table(t)
my_reports = []

#load old reports
old_list = manual_edit.open_reports()
for old_report in old_list:
    old_report[2] = old_report[2].lower()
    determine_dict(old_report)

channel_names = []
for key in HRCBot.user_channels.keys():
    channel_names.append(HRCBot.user_channels[key])
        
print("Logging the reports from " + ', '.join(channel_names)) #change

start_log() #start!
