import json
import time
from core import log


class Main:
    def __init__(self, filename, guild):
        self.users = {}
        self.guild = guild
        self.filename = filename
        self.load_users()

    ##Nick system
    def change_nick(self, user_id, nickname):
        self.users[str(user_id)]['lastChange'] = int(time.time())
        self.users[str(user_id)]['nick'] = nickname
        self.save_users()

    def get_nick(self, user_id):
        nickname = self.users[str(user_id)]['nick']
        if nickname != '':
            return nickname
        else:
            return self.users[str(user_id)]['display_name']

    ##Level system
    def get_lvl(self, user_id):
        return self.users[str(user_id)]['levelsys']

    def change_lvl(self, user_id, lvl, time_in):
        self.users[str(user_id)]['lastChange'] = int(time.time())
        self.users[str(user_id)]['levelsys']['lvl'] = lvl
        self.users[str(user_id)]['levelsys']['time'] = time_in
        self.save_users()

    def change_lvl_display_status(self, user_id, status):
        self.users[str(user_id)]['levelsys']['display'] = status
        self.save_users()

    ##Bansystem
    def add_ban(self, user_id, voicechat, textchat, permanent, for_sek, reason):
        self.users[str(user_id)]['lastChange'] = int(time.time())
        ban_item = {'voicechat': voicechat, 'textchat': textchat, 'permanent': permanent, 'since': int(time.time()), 'for': for_sek, 'reason': reason}
        self.users[str(user_id)]['banned'] = ban_item
        self.save_users()

    def remove_ban(self, user_id):
        self.users[str(user_id)]['lastChange'] = int(time.time())
        self.users[str(user_id)]['banned'] = {}
        self.save_users()

    def get_ban_info(self, user_id):
        info = self.users[str(user_id)]['banned']
        return info

    ##Perms
    def get_perms(self, user_id):
        try:
            return self.users[str(user_id)]['perms']
        except:
            return None

    ##cmdChannel
    def get_cmdChannel(self, user_id):
        try:
            cmdChannel = self.users[str(user_id)]['cmdChannel']
            if cmdChannel != {}:
                return (cmdChannel['channel_name'], cmdChannel['channel_id'])
            else:
                return (None, None)
        except:
            return (None, None)

    def destroy_cmdChannel(self, user_id):
        try:
            self.users[str(user_id)]['lastChange'] = int(time.time())
            self.users[str(user_id)]['cmdChannel'] = {}
            self.save_users()
            return True
        except:
            return False

    def create_cmdChannel(self, user_id, channel_name, channel_id):
        try:
            self.users[str(user_id)]['lastChange'] = int(time.time())
            self.users[str(user_id)]['cmdChannel'] = {"channel_name": channel_name, "channel_id": channel_id}
            self.save_users()
            return True
        except:
            return False

    ##Basics
    def get_users(self):
        return self.users.keys()

    async def reload_users(self, message, cmd, guild, userdb):
        log.log('Info', 'UserDB', 'Reloaded DB...')
        await message.channel.send('Es wurde erfolgreich die User Datenbank reloaded')
        self.load_users()

    def load_users(self):
        json_file = open(self.filename, 'r')
        self.users = json.load(json_file)
        for user in self.guild.members:
            self.add_user(user)
        log.log('Info', 'UserDB', 'Loaded User Database...')

    def save_users(self):
        json_str = json.dumps(self.users, indent=4)
        json_file = open(self.filename, 'w')
        json_file.write(json_str)

    def add_user(self, user):
        if user != None and str(user.id) not in self.users.keys():
            pre_dict = {"createdAt": int(time.time()),
                        "lastChange": int(time.time()),
                        "display_name": user.display_name,
                        "discriminator": user.discriminator,
                        "nick": '',
                        "perms": ['bot.nick', 'bot.lvl'],
                        "cmdChannel": {},
                        "banned": {},
                        "levelsys": {"lvl": 0, "time":  0, "display": False}}
            self.users[str(user.id)] = pre_dict
            self.save_users()
            log.log('Info', 'UserDB', 'The User {0} was added to the Database'.format(user.display_name))
            return True
        else:
            return False

    def update_user(self, user):
        self.users[str(user.id)]['display_name'] = user.display_name
        self.users[str(user.id)]['discriminator'] = user.discriminator
        self.save_users()
        log.log('Info', 'UserDB', 'The User {0} has been updated'.format(user.display_name))

    def remove_user(self, user):
        self.users.pop(str(user.id))
        self.save_users()
        log.log('Info', 'UserDB', 'The User {0} was removed from the Database'.format(user.display_name))