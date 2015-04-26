"""
Created on July, 2014
@author: ma56nin / Matt
Contact: ma56nin@hotmail.com
"""

try:
    import config
except ImportError:
    print("config.py file not found.")

try:
    import customization
    import features
    import slackbot
    import mysqlwork
except ImportError:
    print("customization, features, slackbot or mysqlwork not able to import.")
    exit()

try:
    import time
    import datetime
except ImportError:
    print("time and datetime modules of python were unable to import, check python installation.")
    exit()


def start_log():  # infinite loop, runs main() every minute
    t = time.gmtime()
    while True:
        if time.gmtime()[4] != t[4]:
            bans, cleans = customization.open_files()
            main()
            t = time.gmtime()


def main():
    # Main procedure: gets new messages and logs them
    HRCBot.get_new_messages()
    for new_report in HRCBot.new_reports:
        write_report(new_report)
        mysqlwork.add_records(table, new_report)


def write_report(report):
    # Creates local record for backup
    # inputs:
    # report: [<reporter>, <IGN>, <verdict>, <date in [yyyy,mm,dd]>, <mod-who-banned>]
    b = open("reports_record.dat", "r+")
    b.readlines()
    report_to_write = '\n' + str(report[0]) + "\t" + str(report[1]) + "\t" + str(report[2]) + "\t" + \
                      str(report[3][2]) + "-" + str(report[3][1]) + "-" + str(report[3][0]) + "\t" + report[4]
    b.write(report_to_write)
    b.close()

# Set up report structure
HRCBot = slackbot.Bot()
table = config.table
bans, cleans = customization.open_files()

channel_names = []
for key in HRCBot.user_channels.keys():
    channel_names.append(HRCBot.user_channels[key])

print("Logging the reports from " + ', '.join(channel_names))  # change

start_log()  # start!
