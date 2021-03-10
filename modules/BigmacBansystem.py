import json
import time
import ast

time_str = {'s': 1,
            'm': 60,
            'h': 3600,
            'd': 86400}

class Main:
    def __init__(self, guild, filename):
        self.guild = guild
        self.filename = filename
        self.ban_history = {}
        self.load_ban_history()

    def test_member(self, member_id, type):
        for user in list(self.ban_history):
            if self.ban_history[user]['permanent'] == False and (self.ban_history[user]['since'] + self.ban_history[user]['for']) <= int(time.time()):
                self.ban_history.pop(user)
                self.save_ban_history()

        if member_id in self.ban_history.keys():
            if self.ban_history[member_id]['voicechat'] and type == 'vc' or self.ban_history[member_id]['textchat'] and type == 'tc' or not self.ban_history[member_id]['textchat'] and not self.ban_history[member_id]['textchat']:
                if not self.ban_history[member_id]['permanent']:
                    ban_time = self.ban_history[member_id]['since'] + self.ban_history[member_id]['for'] - int(time.time())
                    return [ban_time, self.ban_history[member_id]['reason']]
                else:
                    return [0, self.ban_history[member_id]['reason']]
            else:
                return [-1, '']
        else:
            return [-1, '']

    def str_to_time(self, str):
        try:
            pos = []
            pos.append(['s', str.find('s')])
            pos.append(['m', str.find('m')])
            pos.append(['h', str.find('h')])
            pos.append(['d', str.find('d')])

            pos_sort = sorted(pos, key=lambda position: position[1])
            timestr = str.replace('s', '#')
            timestr = timestr.replace('m', '#')
            timestr = timestr.replace('h', '#')
            timestr = timestr.replace('d', '#')
            timestr = timestr.split('#')[:-1]
            sek = 0
            a = 0
            for i in range(4-len(timestr), 4):
                sek += int(timestr[a]) * time_str[pos_sort[i][0]]

            return sek
        except:
            return 0

    async def cmd_pardon(self, message, cmd):
        if cmd[1] in self.ban_history:
            self.ban_history.pop(cmd[1])
            self.save_ban_history()
            await message.channel.send('Dieser User wurde erfolgreich entbannt')
        else:
            await message.channel.send('Dieser User wurde nicht gefunden oder wurde nicht gebannt')

    # !ban 703620964667097138 Perm For no Reason
    # !ban 703620964667097138 60s For no Reason
    # !ban vc 703620964667097138 Perm For no Reason
    # !ban tc 703620964667097138 98s For no Reason
    async def cmd_ban(self, message, cmd):
        user_id = ''
        voicechat = False
        textchat = False
        permanent = False
        for_sek = 0
        error = False
        try:
            if cmd[1] == 'vc':
                voicechat = True
            elif cmd[1] == 'tc':
                textchat = True
        except IndexError: await message.channel.send('Der Banntyp oder die UserID fehlt'); error = True


        if voicechat or textchat:
            try: user_id = str(int(cmd[2]))
            except ValueError: await message.channel.send('User ID Error'); error = True
            except IndexError: await message.channel.send('Die User ID Fehlt'); error = True

            try:
                if cmd[3] == 'Perm': permanent = True
                else:
                    for_sek = self.str_to_time(cmd[3])
                    if for_sek == 0:
                        await message.channel.send('Time Error'); error = True
            except IndexError: await message.channel.send('Die Zeit Fehlt'); error = True
            reason = ''
            if cmd[4:] != []:
                for word in cmd[4:]:
                    reason += word + ' '
                reason = reason[:-1]
        else:
            try: user_id = str(int(cmd[1]))
            except ValueError: await message.channel.send('User ID Error'); error = True
            except IndexError: await message.channel.send('Die User ID Fehlt'); error = True

            try:
                if cmd[2] == 'Perm': permanent = True
                else:
                    for_sek = self.str_to_time(cmd[2])
                    if for_sek == 0:
                        await message.channel.send('Time Error'); error = True
            except IndexError: await message.channel.send('Die Zeit Fehlt'); error = True
            reason = ''
            if cmd[3:] != []:
                for word in cmd[3:]:
                    reason += word + ' '
                reason = reason[:-1]

        if not error:
            await message.channel.send('Spieler wird gebannt')
            await self.guild.get_member(int(user_id)).edit(voice_channel=None)
            self.add_to_history(user_id, voicechat, textchat, permanent, for_sek, reason)
        else:
            await message.channel.send('Es gab einen/mehere Fehler bei dem Versuch einen Spieler zu bannen')

    def save_ban_history(self):
        json_str = json.dumps(self.ban_history)
        json_file = open(self.filename, 'w')
        json_file.write(json_str)

    def add_to_history(self, user_id, voicechat, textchat, permanent, for_sek, reason):
        self.ban_history[user_id] = {'voicechat': voicechat, 'textchat': textchat, 'permanent': permanent, 'since': int(time.time()), 'for': for_sek, 'reason': reason}
        self.save_ban_history()

    def load_ban_history(self):
        json_file = open(self.filename, 'r')
        self.ban_history = json.load(json_file)