# -*- coding: utf-8 -*-
"""
Created on February 2015
@author: ma56nin / Matt
@contact: ma56nin@hotmail.com
"""

try:
    import slacker
except ImportError:
    print("slacker not able to import, check installation.")
    exit()

import config


class Bot(object):
    def __init__(self):
        self._get_config()
        self._create_client()
        self._create_channels()
        self._determine_users_of_channel()
        self._create_id_user_database()
        self._get_previous_messages()
        self.new_msgs = {}
        self.mod_lst = []

    def _get_config(self):
        """ Configures the slack bot for the network's Slack """

        self.client_id = config.client_id
        self.client_secret = config.client_secret
        self.code = config.code  # unknown how this works, doesn't seem to matter...
        self.redirect_uri = config.redirect_uri
        self.bot_token = config.bot_token  # HRCBot - requires integration
        self.channel_keyword = config.channel_keyword

    def _create_client(self):
        """ Creates self.client for convenience """

        self.client = slacker.Slacker(self.bot_token)

    def _create_channels(self):
        """ Determines channels to log reports from, channel must have "reports" in its name """

        user_channels = {}
        channels = self.client.channels.list()
        self.channels = channels
        for channel in channels.body['channels']:
            if self.channel_keyword in channel['name']:
                user_channels[channel['id']] = channel['name']
        self.user_channels = user_channels
        # {<id of channel>: <name of channel>}

    def _determine_users_of_channel(self):
        """ Determines which users are in which channel """
        users = {}
        for channel in self.channels.body['channels']:
            users[channel['id']] = channel['members']
        self.users_by_channel = users
        # {<id of chat>: <id of members of chat>}

    def _create_id_user_database(self):
        """ Dictionary to obtain a username from a given ID """
        all_users = { }
        members = self.client.users.list().body['members']
        for member in members:
            all_users[member['id']] = member['name']
        self.user_id_name_database = all_users
        # {<id>: <name>}

    def get_id_from_user(self, username):
        """
        Determines the userID of a given username
        :param username: string - username
        :return: string - user ID
        """

        for user in self.user_id_name_database:
            if self.user_id_name_database[user] == username:
                return user
        return None

    def get_id_of_channel(self, name):
        """
        determines the id of a channel given its common name (debugging purposes)
        :param name: string - common name of the channel
        :return: string - slack ID of the channel
        """

        for key in self.user_channels.keys():
            if self.user_channels[key] == name:
                return key
        return None

    def _get_previous_messages(self):
        """Adds the previous 50 messages to a dictionary to store for later"""
        prev_messages = {}
        for channel in self.channels.body['channels']:
            channel_id = channel['id']
            if channel_id in self.user_channels.keys():
                history_of_channel = self.client.channels.history(channel_id)
                messages_of_channel = history_of_channel.body['messages'][:50]
                prev_messages[channel_id] = messages_of_channel

        self.prev_messages = prev_messages

    def _get_mods(self):
        """
        Determines the moderators of the network for verification purposes
        Anyone with Slack rank 'Admin', 'Owner' or 'Primary Owner' is assumed to be a moderator
        """

        mod_lst = []
        for user in self.client.users.list().body['members']:
            if "is_admin" in user.keys():
                if user['is_admin']:
                    mod_lst.append(user['id'])
        self.mod_lst = mod_lst

    def get_new_messages(self):
        """
        Gets the new messages in the appropriate slack groups, adds to prev_messages and logs them
        """

        self._create_channels()  # Allows for new channels
        channel_lst = self.user_channels
        new_msgs = {}
        
        for channel in channel_lst:
            if len(self.prev_messages[channel]):
                lst_msg_of_channel = self.prev_messages[channel][0]['ts']
                messages = self.client.channels.history(channel, oldest=lst_msg_of_channel)
                if messages is not None:
                    new_msgs[channel] = messages.body['messages']

        self.new_msgs = new_msgs
        self._add_messages()

        self._get_mods()
        return self._log_messages()

    def _add_messages(self):
        """
        Adds messages obtained from get_new_messages to prev_messages and removes old messages
        """

        for key in self.new_msgs.keys():
            if key in self.prev_messages.keys():
                self.prev_messages[key] = self.new_msgs[key] + self.prev_messages[key]

                if len(self.prev_messages[key]) > 50:
                    self.prev_messages[key] = self.prev_messages[key][:50]

    def _log_messages(self):
        """Logs the new messages obtained from get_new_messages in reports"""

        reports = []
        for channel in self.new_msgs.keys():
            for msg in self.new_msgs[channel]:
                if msg['text'][0] == "!":
                    rep = self._make_report(msg, channel)
                    reports.append(rep)

        return reports

    def _make_report(self, msgobj, channel):
        """
        Parses the message into an easily manipulated list for further analysis
        :param msgobj: dictionary - slacker message object
        :param channel: string - ID of the channel the message is in
        :return:
            reporters: list (of strings) - slacker ID(s) of the reporters
            verdict: string - verdict issued by the moderator
            IGN: string - IGN of the player reported
            date: list (of ints) [yyyy, mm, dd] - current date = date of report
            mod: string - slacker ID of the mod who addressed the report
        """

        message = msgobj['text'].split(" ")
        verdict = message[0][1:].lower()
        ign = message[1]

        endpt = min(len(self.prev_messages[channel]), 50)
        
        reporters = []
        rep_names = []
        for msg in self.prev_messages[channel][:endpt]:
            if msg['text'].find(ign) != -1 and msg['user'] not in self.mod_lst:
                reporters.append(msg['user'])
                rep_names.append(self.user_id_name_database[msg['user']])
                if "attachments" in msg.keys():
                    link = msg['attachments'][0]['from_url'].encode('utf-8')
                    if link.find("youtu") == -1:  # don't want a1.kitpvp!
                        link = "NULL"
                else:
                    link = "NULL"
            elif msg['text'].find(ign) != -1 and msg['user'] in self.mod_lst:
                mod = msg['user']

        # Has never been needed, but better safe than crashed (and Pycharm was yelling at me :( )
        if 'mod' not in locals():
            mod = "Unknown"

        if 'link' not in locals():
            link = "NULL"

        return reporters, rep_names, ign, verdict, mod, channel, link

HRCBot = Bot()