class Main:
    def __init__(self, BotPrefix):
        self.BotPrefix = BotPrefix

    async def cmd_create_help(self, message, cmd):
        explizit_cmd = cmd[1:]
        if explizit_cmd != []:
            if explizit_cmd[0] == 'create':
                await message.channel.send('Der **' + self.BotPrefix + 'create** command wird benutzt um einen eigenen Channel zu erstellen.\n'
                                           'Dieser Command funktioniert auch nur in einem vom Owner ausgesuchten Channel\n'
                                           'Jeder User kann nur einen eigenen Channel erstellen. Dafür kann aber auch nur der ersteller Commands senden und lesen.\n'
                                           'Die User mit den **Administrator** Rechten können dies natürlich auch.\n'
                                           'Die Syntax: **' + self.BotPrefix + 'create {Channel name}**')
            elif explizit_cmd[0] == 'destroy':
                await message.channel.send('Der **' + self.BotPrefix + 'destroy** command wird verwendet um deinen eigenen Command Channel zu löschen.\n'
                                           'Du kannst diesen Befehl auch nutzen um alle Nachrichten in deinem Channel zu löschen.\n'
                                           'Natürlich musst du dann wieder einen neuen mit dem **' + self.BotPrefix + 'create** befehl erstellen.\n'
                                           'Die Syntax: **' + self.BotPrefix + 'destroy**')
            else:
                await message.channel.send('Diesen Command gibt es nicht. **' + self.BotPrefix + 'help** um alle verfügbaren commands anzuzeigen')
        else:
            await message.channel.send('Um einen Channel zu erstellen tippe **' + self.BotPrefix + 'create {Channel name}**\n'
                                       'Um deinen Channel wieder zu löschen tippe **' + self.BotPrefix + 'destroy**\n'
                                       'Für explizite Hilfe zu befehlen tippe **' + self.BotPrefix + 'help {command}**')

    async def cmd_help(self, message, cmd):
        explizit_cmd = cmd[1:]
        if explizit_cmd != []:
            if explizit_cmd[0] == 'ban':
                await message.channel.send(self.cmd_ban())
            elif explizit_cmd[0] == 'pardon':
                await message.channel.send(self.cmd_pardon())
            elif explizit_cmd[0] == 'nick':
                await message.channel.send(self.cmd_nick())
            else:
                await message.channel.send('Diesen Command gibt es nicht. **' + self.BotPrefix + 'help** um alle verfügbaren commands anzuzeigen')
        else:
            await message.channel.send('Um einen Spieler zu Bannen tippe **' + self.BotPrefix + 'ban vc/tc/* {Member ID} {Time} {Reason}**\n'
                                       'Um einen Spieler zu entbannen tippe **' + self.BotPrefix + 'pardon {Member ID}**\n'
                                       'Um dir selbst einen neuen nickname zu geben tippe **' + self.BotPrefix + 'nick {new nickname}**\n'
                                       'Für explizite Hilfe zu befehlen tippe **' + self.BotPrefix + 'help {command}**')

    def cmd_ban(self):
        message = 'Der **' + self.BotPrefix + 'ban** command wird verwendet um spieler zu bannen.\n' \
                                              'Dies funktionier Temporär sowie auch Permanent\n' \
                                              'Um einen spieler Temporär zu bannen gibt man als **{Time}** etwas wie 9h60m an\n' \
                                              'hier steht **d** für Tage, **h** für Stunden, **m** für minuten und **s** für sekunden.\n' \
                                              'Um jemanden Permanent zu bannen gibt man **Perm** an für **{Time}**\n' \
                                              'Um jemanden nur für den VoiceChat zu bannen gibt man vor der **{Member ID}** **vc** an für den TextChat **tc**\n' \
                                              'Einen Grund für den bann kann man nennen muss man aber nicht. Dies tut man aber am ende des Commands\n' \
                                              'Die Syntax: **' + self.BotPrefix + 'ban vc/tc/* {Member ID} {Time} {Reason}**'

        return message

    def cmd_pardon(self):
        message = 'Der **' + self.BotPrefix + 'pardon** command wird verwendet um die gebannt member wieder zu entbannen\n' \
                                              'Dieser funktioniert auch wenn der Spieler Permanent gebannt worden ist.\n' \
                                              'Die Syntax: **' + self.BotPrefix + 'pardon**'

        return message

    def cmd_nick(self):
        message = 'Der **' + self.BotPrefix + 'nick** command wird verwendet um seinen eigenen Nickname zu ändern\n' \
                                              'Die Syntax: **' + self.BotPrefix + 'nick {new Nickname}**'

        return message