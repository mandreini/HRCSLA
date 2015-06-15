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
    import features
    import slackbot
    import mysqlwork
except ImportError:
    print("features, slackbot or mysqlwork not able to import.")
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
        if time.gmtime()[2] != t[2]:
            mysqlwork.remove_duplicates(table)
        if time.gmtime()[4] != t[4]:
            main()
            t = time.gmtime()


def main():
    """ Main procedure: gets new messages and logs them """
    # try:
    new_reports = hrcbot.get_new_messages()
    for new_report in new_reports:
        if not mysqlwork.check_for_existing_report(new_report):
            write_report(new_report)
            mysqlwork.add_records(table, new_report)
    # except:
    #     print "Connection failed"


def write_report(report):
    """ Creates local record for backup
    :param report: [reporter, IGN, verdict, date in [yyyy,mm,dd], mod_who_banned]
        reporter: string - userID of the reporter
        IGN: string - IGN of the player reported
        verdict: string - verdict of the mod
        date: list (of ints) - date of the report
        mod_who_banned: string - userID of the mod who addressed the report"""

    b = open("reports_record.dat", "r+")
    b.readlines()
    report_to_write = '\n' + str(report[0]) + "\t" + str(report[1]) + "\t" + str(report[2]) + "\t" + \
                      str(report[3][2]) + "-" + str(report[3][1]) + "-" + str(report[3][0]) + "\t" + report[4]
    b.write(report_to_write)
    b.close()

# Set up report structure
hrcbot = slackbot.Bot()
table = config.table

# verdicts
bans = ["banned", "b&", "b4nned"]
cleans = ["clean"]
kicks = ["kicked"]
mutes = ["mutes"]

channel_names = []
for key in hrcbot.user_channels.keys():
    channel_names.append(hrcbot.user_channels[key])

print("Logging the reports from " + ', '.join(channel_names))

start_log()  # start!
