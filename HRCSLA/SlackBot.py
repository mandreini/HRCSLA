# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 17:51:01 2015

@author: Matt
"""

try:
    import slacker
except:
    print("slacker not able to import, check installation.")
    exit
    
import datetime

todo = [
    "configure for getting reporter, IGN, verdict and mod-who-banned from !banned",
    "remove thumbnail (<www.youtube.com...> gives thumbnail, www.youtube.com... doesn't)",]

class Bot(object):
    def __init__(self):
        self.client_id = "3579912104.3705547397"
        self.client_secret = "08f43b21db1ac1110b54f767478e85f1"
        self.code = "?"
        self.redirect_uri = "https://hackerreports.slack.com/messages/global/"
        self.token = "xoxp-3579912104-3698584616-3705527605-602df4"
        self.bot_token = "xoxb-3722743179-PY2jYWOJWBWZpHgBmP8wrGOp"

        self.create_client()
        self.create_channels()
        self.determine_users_of_channel()
        self.create_ID_user_database()
        self.get_previous_messages()
        
    def create_client(self):
        self.client = slacker.Slacker(self.token)
    
    def create_channels(self):
        user_channels = {}
        channels = self.client.channels.list()
        self.channels = channels
        for channel in channels.body['channels']:
            if channel['name'] != "global" and channel['name'] != "help": #and channel['name'] != "meta":
                user_channels[channel['id']] = channel['name']
        self.user_channels = user_channels
        # {<id of channel>: <name of channel>}

    def determine_users_of_channel(self):
        users = {}        
        for channel in self.channels.body['channels']:
            users[channel['id']] = channel['members'] 
        self.users_by_channel = users
        #{<id of chat>: <id of members of chat>}
    
    def create_ID_user_database(self):
        all_users = {}
        members = self.client.users.list().body['members']
        for member in members:
            all_users[member['id']] = member['name']            
        self.user_id_name_database = all_users
        # {<id>: <name>}
                
    def get_id_of_channel(self,name):
        for key in self.user_channels.keys():
            if self.user_channels[key] == name:
                return key
        return "Key not found"        
        
    def get_previous_messages(self):            
        prev_messages = {}
        for channel in self.channels.body['channels']:
            channel_id = channel['id']
            if channel_id in self.user_channels.keys():
                history_of_channel = self.client.channels.history(channel_id)
                messages_of_channel = history_of_channel.body['messages']
                prev_messages[channel_id] = messages_of_channel
            
        self.prev_messages = prev_messages
        
    def get_mods(self):
        mod_lst = []
        for user in self.client.users.list().body['members']:
            if "is_admin" in user.keys():            
                if user['is_admin']:
                    mod_lst.append(user['id'])
        self.mod_lst = mod_lst
        
    def get_new_messages(self):
        channel_lst = self.prev_messages.keys()
        lst_msgs = {}
        new_msgs = {}
        
        for channel in channel_lst:
            lst_msgs[channel] = self.prev_messages[channel][0]['ts']
            
        for channel in channel_lst:
            lst_msg_of_channel = lst_msgs[channel]
            messages = self.client.channels.history(channel, oldest=lst_msg_of_channel)
            new_msgs[channel] = messages.body['messages']
            
        self.new_msgs = new_msgs
        self.get_previous_messages() #is going to be slow
        
        self.get_mods()
        self.log_messages()
        
    def log_messages(self):
        reports = []
        for channel in self.new_msgs.keys():
            for msg in self.new_msgs[channel]:
                if msg['text'][0] == "!" and \
                   msg['user'] in self.mod_lst:
                        reporters, verdict, IGN, date, mod = \
                          self.make_report(msg, channel)
                        for reporter in reporters:
                            reports.append([reporter, IGN, verdict, date, mod])
                else:
                    print msg['text'], msg['user']
                        
        self.new_reports = reports
                
    def make_report(self, msgobj, channel):
        #a Slack message dictionary
        message = msgobj['text'].split(" ")
        verdict = message[0][1:]
        IGN = message[1]
        
        if len(self.prev_messages[channel]) > 50:
            endpt = 50
        else:
            endpt = len(self.prev_messages[channel])
        
        reporters = []
        for msg in self.prev_messages[channel][:endpt]:
            if msg['text'].find(IGN) != -1 and msg['user'] not in self.mod_lst:
                reporters.append(msg['user'])
            elif msg['text'].find(IGN) != -1 and msg['user'] in self.mod_lst:
                mod = msg['user']
                
        now = datetime.datetime.now()
        date = [now.year, now.month, now.day]
        
        return reporters, verdict, IGN, date, mod
        
HRCBot = Bot()
        