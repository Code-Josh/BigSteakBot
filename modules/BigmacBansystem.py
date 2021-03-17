import time
from modules import tools

class Main:
    def __init__(self, guild, userdb):
        self.guild = guild
        self.userdb = userdb

    def get_ban_info(self, member_id, type):
        for user in self.userdb.get_users():
            baninfo = self.userdb.get_ban_info(user)
            if baninfo != {} and baninfo['permanent'] == False and (baninfo['since'] + baninfo['for']) <= int(time.time()):
                self.userdb.remove_ban(str(member_id))

        if str(member_id) in self.userdb.get_users():
            baninfo = self.userdb.get_ban_info(str(member_id))
            if baninfo != {}:
                if baninfo['voicechat'] and type == 'vc' or baninfo['textchat'] and type == 'tc' or not baninfo['textchat'] and not baninfo['textchat']:
                    if not baninfo['permanent']:
                        ban_time = baninfo['since'] + baninfo['for'] - int(time.time())
                        return [ban_time, baninfo['reason']]
                    else:
                        return [0, baninfo['reason']]
            else:
                return [-1, '']
        else:
            return [-1, '']

    def test_member(self, member_id, type):
        ban_info = self.get_ban_info(member_id, type)
        if ban_info[0] != -1:
            message = '-------------------------------------------------------------\n'
            if type == 'tc':
                message += 'Hi du hast versucht eine Textnachricht zu schreiben jedoch wurdest du gebannt und hast keine berechtigung hier zu schreiben.\n'
                if ban_info[0] == 0:
                    message += 'Du wurdest jedoch Permanent gebannt, ohne das die Admins dich wieder entbannen wirst du keine Nachrichten mehr schreiben können.\n'
                else:
                    message += 'Es dauert noch {0} bis du die berechtigung wieder bekommst.\n'.format(tools.time_to_str(ban_info[0]))

                if ban_info[1] != '':
                    message += 'Bann Grund: {0}'.format(ban_info[1])
            elif type == 'vc':
                message += 'Hi du hast versucht in einen VoiceChannel zu gehen, da du gebannt wurdest hast du dafür keine Berechtigung\n'
                if ban_info[0] == 0:
                    message += 'Du wurdest jedoch Permanent gebannt, ohne das die Admins dich wieder entbannen wirst du nicht mehr in VoiceChannels gehen können.\n'
                else:
                    message += 'Es dauert noch {0} bis du die berechtigung wieder bekommst.\n'.format(tools.time_to_str(ban_info[0]))

                if ban_info[1] != '':
                    message += 'Bann Grund: {0}\n'.format(ban_info[1])
            return [True, message]
        else:
            return [False, '']

    async def cmd_pardon(self, message, cmd, guild, userdb):
        if cmd[1] in self.ban_history:
            self.userdb.remove_ban(cmd[1])
            await message.channel.send('Dieser User wurde erfolgreich entbannt')
        else:
            await message.channel.send('Dieser User wurde nicht gefunden oder wurde nicht gebannt')

    # !ban 703620964667097138 Perm For no Reason
    # !ban 703620964667097138 60s For no Reason
    # !ban vc 703620964667097138 Perm For no Reason
    # !ban tc 703620964667097138 98s For no Reason
    async def cmd_ban(self, message, cmd, guild, userdb):
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
                if cmd[3].lower() == 'perm': permanent = True
                else:
                    for_sek = tools.str_to_time(cmd[3])
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
                if cmd[2].lower() == 'perm': permanent = True
                else:
                    for_sek = tools.str_to_time(cmd[2])
                    if for_sek == 0:
                        await message.channel.send('Time Error'); error = True
            except IndexError: await message.channel.send('Die Zeit Fehlt'); error = True
            reason = ''
            if cmd[3:] != []:
                for word in cmd[3:]:
                    reason += word + ' '
                reason = reason[:-1]

        if not error:
            if str(user_id) in self.userdb.get_users():
                await message.channel.send('Spieler wird gebannt')
                await self.guild.get_member(int(user_id)).edit(voice_channel=None)
                self.userdb.add_ban(user_id, voicechat, textchat, permanent, for_sek, reason)

                dm_channel = await self.guild.get_member(int(user_id)).create_dm()

                message_dm = '-------------------------------------------------------------\n' \
                                      'Hey du wurdest gebannt, warscheinlich hast du abgefuckt oder hast etwas Falsch gemacht\n' \
                                      'Falls du nicht weist warum du genau gebannt wurdest Frag: **{0}** per DM welcher dich gebannt hat\n'.format(self.guild.get_member(message.author.id).display_name)
                if permanent:
                    message_dm += 'Du wurdest Permanent gebannt somit kannst du ohne das dich ein Admin entbannt nichts mehr auf diesem Server machen\n'
                else:
                    message_dm += 'Du wurdest für {0} gebannt\n'.format(tools.time_to_str(for_sek))

                if reason != '':
                    message_dm += 'Grund: ' + reason

                await dm_channel.send(message_dm)
            else:
                await message.channel.send('Dieser Spieler existiert nicht')
        else:
            await message.channel.send('Es gab einen/mehere Fehler bei dem Versuch einen Spieler zu bannen')