"""
Created on July, 2014
@author: ma56nin9 / Matt
Contact: ma56nin@hotmail.com
"""

import time
import datetime

#old-new skype database
##def get_oldSkype_newSkype(d):
##    #creates dictionary to allow old skypes to be transfered to new skypes
##    #input, "filename.txt" of database with first 2 lines commented out
##    layover = {}    
##    f = open(d,"r")
##    lines = f.readlines()[2:]
##    f.close()    
##    
##    lines = [i.strip('\n') for i in lines]
##    lines = [i.split("**") for i in lines]
##    current_skype = [i[0] for i in lines]
##    old_skypes = [i[1:] for i in lines]
##    
##    for player in range(len(old_skypes)):
##        for alt in old_skypes[player]:
##            layover[alt] = current_skype[player]
##            
##    return layover #dictionary: {<old1>: <new1>, <old2>: <new1>, <old3>: <new2>...}
    
##def check_for_new(skype,layover):
##    #checks if the given skype has an updated version
##    #inputs: skypeaccount (string), layover layover #dictionary: {<old1>: <new1>, <old2>: <new1>, <old3>: <new2>...}
##    if skype in layover.keys():
##        return layover[skype]
##    return skype #string - current skype    
    
#keeping track of mod and player activity
def combine_players(name_list):
    #combines the list of people in HRC into 1 list
    #inputs: list of chats of HRC, each chat is a list of strings of player handles
    #[ [<HRC chat name 1>, <player1>, <player2> ...], [<HRC chat name 2>, <playera>, ...]...]
    names = []
    for chat in name_list:
        for name in chat[1:]:
            if name not in names:
                names.append(name)
    return names #[<player1>, <player2>, ...]

def get_activity(Running_list): #very slow
    #determines who has posted a message in the past month
    #inputs: Running_list generated by main.py - a dictionary
    #{<HRC chat 1>: [chatmessage-1, chatmessage-2, ... chatmessage0], <HRC chat 2>: [chatmessage-1, ...]...}
    month = time.gmtime()[1] - 1
    year = time.gmtime()[0]
    if month == 0:
        month = 12
        year -= 1
    senders = {}
    chatmsgs = [Running_list[i] for i in Running_list.keys()]
    for chat in chatmsgs:
        for msg in chat:
            if msg.Datetime.month == month and msg.Datetime.year == year:
                if msg.Sender not in senders.keys():
                    senders[msg.Sender] = 0
                senders[msg.Sender] += 1
    return senders #dictionary - {<player1>: x1, <player2>: x2, ...}
    
def get_inactive_players(name_list, Running_list):
    #determines who is inactive / hasn't posted a single message
    #inputs same as combine_players and get_activity
    players = combine_players(name_list)
    activity = get_activity(Running_list)
    inactives = []
    for player in players:
        if player not in activity.keys():
            inactives.append(player.Handle)
    return inactives #list of strings of handles of inactive players (including mods)
    #limitations: Xx_Randy_PvP_xX can avoid this list with "hi guys" at the start of the month and nothing more

def get_mod_activity(mods, records, timeframe=-1): #untested
    #this is mainly to see which mods are most active, get them in more HRC chats
    #inputs: list of mods, list of reports (including mod-who-banned) = [[<reporter>, <IGN>, <verdict>, <mod_who_banned>, [dd,mm,yyy]], ... ]
    #timeframe is number of days, -1 is all time, 0 is current day, 1 is yesterday etc
    mod_activity = {}
    for report in records:
            mod_who_banned = report[3]
            if timeframe == -1:
                if mod_who_banned not in mod_activity.key():
                    mod_activity[mod_who_banned] = 0
                mod_activity[mod_who_banned] += 1
            else:
                date_of = datetime.datetime(report[4][2],report[4][1],report[4][0])
                ddif = abs((datetime.datetime.now() - date_of).days) 
                if ddif <= timeframe:
                    if mod_who_banned not in mod_activity.key():
                        mod_activity[mod_who_banned] = 0
                    mod_activity[mod_who_banned] += 1
    return mod_activity #dictionary {<mod1>: y1, <mod2>: y2, ...}

def add_potential_mod(poster, verdict, message): #adds a player who gave a banned/clean verdict to the potential mods file
    try:
        f = open("potential_mods.txt","r+")
    except:
        print("potential_mods.txt not found, creating a new one...")
        f = open("potential_mods.txt","w+")
    f.readlines()
    f.write("\n" + poster + ": " + verdict + " on '" + message + "'")
    f.close()
