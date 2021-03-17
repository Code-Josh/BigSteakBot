from core import log
from modules import tools
import asyncio
import discord

class Main:
    def __init__(self, userdb, guild):
        self.userdb = userdb
        self.guild = guild

    def update_level(self, user_id):
        current_lvl = self.userdb.get_lvl(user_id)
        time_int = current_lvl['time']
        time_int += 60
        lvl = time_int // 86400
        self.userdb.change_lvl(user_id, lvl, time_int)

    async def test_members(self):
        while True:
            for userid in self.userdb.get_users():
                user = self.guild.get_member(int(userid))
                if user != None:
                    if user.voice != None and not user.voice.self_mute and not user.voice.self_deaf:
                        self.update_level(userid)
                lvl = self.userdb.get_lvl(userid)
                if lvl['display']:
                    await self.update_nick(userid)
            await asyncio.sleep(60)

    async def update_nick(self, user_id):
        try:
            user = self.guild.get_member(int(user_id))
            lvl = self.userdb.get_lvl(user_id)
            if lvl['display']:
                nickname = '[Lvl: {0}] '.format(lvl['lvl']) + self.userdb.get_nick(str(user_id))
            else:
                nickname = self.userdb.get_nick(str(user_id))
            await user.edit(nick = nickname)
        except discord.errors.Forbidden:
            log.log('Error', 'Nicksys', 'Missing Permissions for changing Nickname')


    async def cmd_lvl(self, message, cmd, guild, userdb):
        if len(cmd) >= 2:
            if cmd[1] == 'get':
                lvl = self.userdb.get_lvl(message.author.id)
                if lvl['time'] == 0:
                    lvl_str = '0m'
                else:
                    lvl_str = tools.time_to_str(int(lvl['time']))
                await message.channel.send('Dein aktuelles Level ist: {0}, Deine verbrachte Zeit auf dem Server: {1}'.format(lvl['lvl'], lvl_str))
            elif cmd[1] == 'display':
                if len(cmd) >= 3:
                    if cmd[2] == 'on':
                        self.userdb.change_lvl_display_status(message.author.id, True)
                        await self.update_nick(str(message.author.id))
                        await message.channel.send('Der Status wurde erfolgreich geändert')
                    elif cmd[2] == 'off':
                        self.userdb.change_lvl_display_status(message.author.id, False)
                        await self.update_nick(str(message.author.id))
                        await message.channel.send('Der Status wurde erfolgreich geändert')
                else:
                    await message.channel.send('Du musst hinter dem command noch den status setzen')
            else:
                await message.channel.send('Diesen Command gibt es nicht für hilfe **"!help lvl"**')
        else:
            await message.channel.send('Dieser Command benötigt noch einen sub-command wie: **get** oder **display**')

    async def cmd_nick(self, message, cmd, guild, userdb):
        try:
            cmd_after = ''
            for cmd_a in cmd[1:]:
                cmd_after += ' ' + cmd_a
            cmd_after = cmd_after[1:]
            if cmd_after == '':
                await message.channel.send('Du muss hinter **"!nick"** deinen neuen nickname schreiben')
            else:
                self.userdb.change_nick(message.author.id, cmd_after)
                await self.update_nick(message.author.id)
                log.log('Info', 'Nick',
                        'Der User {0} hat seinen Nickname zu {1} verändert'.format(message.author.name,
                                                                                   cmd_after))
                await message.channel.send('Dein nickname wurde erfolgreich zu **{0}** geändert'.format(cmd_after))
        except:
            await message.channel.send(
                'Bei diesem Befehl entstand ein Fehler bitte kontaktiere den Server-Owner/Bot-Owner')
