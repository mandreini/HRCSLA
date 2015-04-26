"""
Created on July, 2014
@author: ma56nin9 / Matt
Contact: ma56nin@hotmail.com
"""

import mysqlwork
import datetime
import slackbot
import config

def get_activity(table, user, mod_list, time_frame=-1):
    # gets the activity of a given user
    # probably will change to a web-based system with the UI separate of the process (or !activity <name>)
    # inputs:
        # table: string - name of the table
        # user: string - Slack user ID
        # mod_list: list - list of mods (from SlackBot.Bot().get_mods() procedure)
        # time_frame: time_frame of activity, if empty (-1), then all activity
    if user in mod_list:
        cat = "ModID"
        isMod = True
    else:
        cat = "UserID"
        isMod = False

    count, act_list = mysqlwork.retrieve_values(table, user, time_frame, cat)

    # probably will change...
    if count == 0:
        return "No activity found for %s" % user
    else:
        if isMod:
            return "The mod, " + user + " has addressed " + count + " reports. These reports are: \n" + "\n".join(act_list)
        else:
            return "The reporter, " + user + " has reported " + count + " reports. These reports are: \n" + "\n".join(act_list)

def remove_report(ign, userid):
    # This will remove a report from the database given the IGN of the hacker. ONLY for mod use with !remove
    # Will remove the the first entry found (i.e. if !clean but then !banned later, !remove)
    # inputs:
        # IGN: string - IGN of the hacker to be removed

    if mysqlwork.remove_row(ign):
        message = "Report successfully removed!"
        slackbot.HRCBot.send_dm(userid, message)
        pass

def add_report(message, channel):
    # This will allow reports to be added to the database
    # Syntax: !add <reporter> <ign> <verdict>
    # inputs:
        # message: slacker message object - message object of the !add message
        # channel: string - ID of the channel the message was posted in
    msg = message['text']
    parsedmsg = msg.split(" ")
    reporter = parsedmsg[1]
    ign = parsedmsg[2]
    verdict = parsedmsg[3]
    mod = message['user']
    link = "NULL"

    report = [reporter, ign, verdict, mod, channel, link]
    mysqlwork.add_records(config.table, report)
    # Either direct message or some way to confirm that the report was added successfully