import json
from core import user

class Main:
    def __init__(self, guild, userdb, cmd_category_name):
        self.guild = guild
        self.cmd_channels = None
        self.channel_authors = []
        self.channel_names = []
        self.channel_ids = []
        self.userdb = userdb
        self.load_cmd_channels()
        self.cmd_category = self.guild.get_channel(cmd_category_name)

    async def cmd(self, message):
        cmd = message.content.split(' ')
        if cmd[0] == 'create':
            try:
                wert = await self.create_cmd_channel(message.author, cmd[1])
            except IndexError:
                pass
                wert = 4
            if wert == 0:
                await message.channel.send(
                    'Ein unerwarteter Fehler kam zu stande als versucht wurde den Command-Channel **{0}** zu erstellen'.format(
                        cmd[1]))
            elif wert == 1:
                await message.channel.send('Der Command-Channel **{0}** wurde erfolgreich erstellt'.format(cmd[1]))
            elif wert == 2:
                await message.channel.send('Du kannst nur einen Command-Channel erstellen'.format(cmd[1]))
            elif wert == 3:
                await message.channel.send('Diesen namen gibt es schon, versuchs mit einem anderen'.format(cmd[1]))
            elif wert == 4:
                await message.channel.send('Du musst hinter **"!create"** einen namen hinzufügen')
        elif cmd[0] == 'destroy':
            wert = await self.destroy_cmd_channel(message.author)
            if wert == 0:
                await message.channel.send(
                    'Ein unerwarteter Fehler kam zu stande als du versucht hast dein Command-Channel zu erstellen')
            elif wert == 1:
                await message.channel.send('Dein Command-Channel wurde erfolgreich gelöscht')
            elif wert == 2:
                await message.channel.send('Du hast keinen Command-Channel welchen man löschen kann')
        else:
            await message.channel.send('Diesen Command gibt es nicht für hilfe **"!help"**')


    async def create_cmd_channel(self, user, channel_name):
        channel_name = 'cmd┃' + channel_name
        if str(user.id) in self.channel_authors:
            return 2
        if channel_name in self.channel_names:
            return 3
        else:
            try:
                channel = await self.guild.create_text_channel(channel_name, category=self.cmd_category)
                await channel.set_permissions(user, read_messages=True, send_messages=True)
                await channel.set_permissions(self.guild.roles[0], read_messages=False, send_messages=False)

                self.channel_authors.append(str(user.id))
                self.channel_names.append(str(channel.name))
                self.channel_ids.append(str(channel.id))

                self.userdb.create_cmdChannel(str(user.id), str(channel.name), str(channel.id))

                return 1
            except:
                return 0


    async def destroy_cmd_channel(self, user):
        try:
            channelName, channelId = self.userdb.get_cmdChannel(user.id)
            channel_obj = self.guild.get_channel(int(channelId))
            await channel_obj.delete()
            self.userdb.destroy_cmdChannel(str(user.id))

            self.channel_authors.remove(str(user.id))
            self.channel_names.remove(channelName)
            self.channel_ids.remove(channelId)
            return 1
        except:
            return 0

    def load_cmd_channels(self):
        for user in self.userdb.get_users():
            channelName, channelId = self.userdb.get_cmdChannel(user)
            if channelId != None:
                self.channel_authors.append(user)
                self.channel_names.append(channelName)
                self.channel_ids.append(channelId)