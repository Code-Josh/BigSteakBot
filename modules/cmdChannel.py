import json

class Main:
    def __init__(self, guild, filename, cmd_category_name):
        self.guild = guild
        self.cmd_channels = None
        self.channel_authors = []
        self.channel_names = []
        self.channel_ids = []
        self.filename = filename
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
            #try:
            if True:
                channel = await self.guild.create_text_channel(channel_name, category=self.cmd_category)
                await channel.set_permissions(user, read_messages=True, send_messages=True)
                await channel.set_permissions(self.guild.roles[0], read_messages=False, send_messages=False)

                self.channel_authors.append(str(user.id))
                self.channel_names.append(str(channel.name))
                self.channel_ids.append(str(channel.id))
                self.cmd_channels['channels'].append(
                    {"channel_name": str(channel.name), "channel_author_id": str(user.id), "channel_id": str(channel.id)})
                self.save_cmd_channels(self.cmd_channels)
                return 1
            #except:
            #    return 0


    async def destroy_cmd_channel(self, user):
        for channel in self.cmd_channels['channels']:
            if channel['channel_author_id'] == str(user.id):
                try:
                    channel_obj = self.guild.get_channel(int(channel['channel_id']))
                    await channel_obj.delete()
                    self.cmd_channels['channels'].remove(channel)
                    self.channel_authors.remove(channel['channel_author_id'])
                    self.channel_names.remove(channel['channel_name'])

                    self.channel_ids.remove(channel['channel_id'])

                    self.save_cmd_channels(self.cmd_channels)
                    return 1
                except:
                    return 0
        return 2

    def load_cmd_channels(self):
        json_file = open(self.filename, 'r')
        self.cmd_channels = json.load(json_file)
        try:
            for channel in self.cmd_channels['channels']:
                self.channel_authors.append(channel['channel_author_id'])
                self.channel_names.append(channel['channel_name'])
                self.channel_ids.append(channel['channel_id'])
        except KeyError:
            pass


    def save_cmd_channels(self, json_dict):
        json_str = json.dumps(json_dict)
        json_file = open(self.filename, 'w')
        json_file.write(json_str)