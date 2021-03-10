# jeder befahl kann in der config geändert werden genauso wie auch die permission node
#user können voicechannels erstellen
# console log system
#log system
#music bot
# permissionssystem

from modules import tempChannels, cmdChannel, tools, help
from modules import BigmacBansystem as BB
from core import Permissions, config
import discord.client

configFile = 'config.ini'
config_obj = config.Main(configFile)
config_data = config_obj.get_config()

class Main(discord.Client):
    async def on_ready(self):
        print('Api version: {0}.{1}.{2}'.format(discord.version_info.major, discord.version_info.minor, discord.version_info.micro))
        print('Logged in as: {0}'.format(self.user))
        print('Latency: {0}ms'.format(str(self.latency * 1000).split('.')[0]))
        self.appInfo = await self.application_info()
        print('I\'m owned by: {0}'.format(self.appInfo.owner))

        self.config = config_data

        self.guild = self.guilds[0]

        self.tempChan = tempChannels.Main(self.guild)
        for cat in self.config.TempCategorys:
            self.tempChan.add_category(cat[0], cat[1])

        self.cmdChan = cmdChannel.Main(self.guild, self.config.cmdChannelsFile, self.config.cmdCategory_id)

        self.BBansystem = BB.Main(self.guild, self.config.bannedMembersFile)
        self.Perms = Permissions.Main(self.config.permsFile)

        self.help = help.Main(self.config.BotPrefix)
        
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Ver. 1.1'))

        self.commands = {
            'nick': [True, tools.cmd_nick, 'bot.nick'],
            'ban': [True, self.BBansystem.cmd_ban, 'bot.ban'],
            'pardon': [True, self.BBansystem.cmd_pardon, 'bot.pardon']
        }

    async def on_message(self, message):
        check_result = self.BBansystem.test_member(str(message.author.id), 'tc')
        if check_result[0] != -1:
            await message.delete()
            dm_channel = await message.author.create_dm()
            message = '-------------------------------------------------------------\n'
            message += 'Hi du hast versucht eine Textnachricht zu schreiben jedoch wurdest du gebannt und hast keine berechtigung hier zu schreiben.\n'
            if check_result[0] == 0:
                message += 'Du wurdest jedoch Permanent gebannt, ohne das die Admins dich wieder entbannt wirst du keine Nachrichten mehr schreiben können.\n'
            else:
                message += 'Es dauert noch {0:3.3f}h bis du wieder auf diesem Server schreiben darfst.\n'.format(check_result[0] / 3600)

            if check_result[1] == '':
                message += 'Für dein Bann wurde kein Grund gennant'
            else:
                message += 'Bann Grund: {0}'.format(check_result[1])
            await dm_channel.send(message)

        else:
            if message.content.startswith(self.config.BotPrefix):
                message.content = message.content[len(self.config.BotPrefix):]
                if message.channel.id == self.config.createCMDChannel_id:
                    if message.content.startswith('help'):
                        await self.help.cmd_create_help(message, message.content.split(' '))
                    else:
                        await self.cmdChan.cmd(message)
                elif str(message.channel.id) in self.cmdChan.channel_ids:
                    await self.channel_commands(message)

    async def on_voice_state_update(self, member, before, after):
        check_result = self.BBansystem.test_member(str(member.id), 'vc')
        if after.channel != None:
            if check_result[0] != -1:
                await member.edit(voice_channel=None)
                dm_channel = await member.create_dm()
                message = '-------------------------------------------------------------\n'
                message += 'Hi du hast versucht in einen VoiceChannel zu gehen, da du gebannt wurdest hast du dafür keine Berechtigung\n'
                if check_result[0] == 0:
                    message += 'Du wurdest jedoch Permanent gebannt, ohne das die Admins dich wieder entbannen wirst du nicht mehr in VoiceChannels gehen können.\n'
                else:
                    message += 'Es dauert noch {0:3.3f}h bis du wieder auf diesem Server reden kannst.\n'.format(check_result[0] / 3600)

                if check_result[1] == '':
                    message += 'Für dein Bann wurde kein Grund gennant'
                else:
                    message += 'Bann Grund: {0}'.format(check_result[1])
                await dm_channel.send(message)

        if self.config.TempChannels:
            await self.tempChan.voicechannel_update()

    async def channel_commands(self, message):
        cmd = message.content.split(' ')
        if cmd[0] == 'help':
            await self.help.cmd_help(message, cmd)
        else:
            try:
                if self.Perms.test_user(message.author.id, self.commands[cmd[0]][2]):
                    if self.commands[cmd[0]][0]: await self.commands[cmd[0]][1](message, cmd)
                    else: await message.channel.send('Entschuldigung aber dieser Command ist Deaktiviert')
                else:
                    await message.channel.send('Du hast keine Rechte um diesem Command auszuführen')
            except KeyError:
                await message.channel.send('Diesen Command gibt es nicht für hilfe **"!help"**')

intents = discord.Intents(messages=True, guilds=True, members=True, voice_states=True)
bot = Main(intents=intents)
bot.run(config_data.BotSecret)
