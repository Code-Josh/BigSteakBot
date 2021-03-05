from modules import tempChannels, cmdChannel, tools
import discord.client
import json

class Bot:
    token='Nzk4NTU1NzQxMzUzOTM0OTIw.X_2u_Q.J4VwMQDGE58_HsBTWY9fPVpXKNs'

TempChannels_on = True
CommandChannels_on = True

Bot_Prefix = '!'
create_cmdChannel_id = 817345256055898134
cmd_category_id = 817054144866025473

cmdChannelsFile = 'cmd_channels.json'

commands = {
    'nick': [True, tools.cmd_nick]
}

class Main(discord.Client):
    async def on_ready(self):
        print('Api version: {0}.{1}.{2}'.format(discord.version_info.major, discord.version_info.minor, discord.version_info.micro))
        print('Logged in as: {0}'.format(self.user))
        print('Latency: {0}ms'.format(str(self.latency * 1000).split('.')[0]))
        self.appInfo = await self.application_info()
        print('I\'m owned by: {0}'.format(self.appInfo.owner))

        self.guild = self.guilds[0]

        self.tempChan = tempChannels.Main(self.guild)
        self.tempChan.add_category('I am Groot', 'Shitty Talk┃#{0}')
        self.tempChan.add_category('We are Groot', 'Some others❤┃#{0}')

        self.cmdChan = cmdChannel.Main(self.guild, cmdChannelsFile, cmd_category_id)

    async def on_message(self, message):
        if message.content.startswith(Bot_Prefix):
            message.content = message.content[len(Bot_Prefix):]
            if message.channel.id == create_cmdChannel_id:
                await self.cmdChan.cmd(message)
            elif str(message.channel.id) in self.cmdChan.channel_ids:
                await self.channel_commands(message)

    async def on_voice_state_update(self, member, before, after):
        if TempChannels_on:
            await self.tempChan.voicechannel_update()

    async def channel_commands(self, message):
        cmd = message.content.split(' ')
        try:
            if commands[cmd[0]][0]: await commands[cmd[0]][1](message, cmd)
            else: await message.channel.send('Entschuldigung aber dieser Command ist Deaktiviert')
        except KeyError:
            await message.channel.send('Diesen Command gibt es nicht für hilfe **"!help"**')

intents = discord.Intents(messages=True, guilds=True, members=True, voice_states=True)
bot = Main(intents=intents)
bot.run(Bot.token)
