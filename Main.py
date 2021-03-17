#besseres fehlerhandling für die console/discord
#bessere discord Fehlermeldungen

#v 1.1.2
#usersystem +
#beim bannen kommt eine nachricht an den gebannten spieler +
#die nachricht wird im bigmac system erstellt nicht in Main.py +
#sek to str +

#nicksystem (vorbereitung für level system) +
#level system wie tobi +

#log in der console +
#log in einer datei +
#v 1.1.3 (stability/utility update)
# logging via logging module
# mehr info logs
# mehr error/warning logs
# leichtes permissions system mit implementierung von commands
# config system überarbeiten
# user system überarbeiten(user obj welches ausgegeben wird anstatt 1000 funktionen für jede einstellung)
# erweitertes help system(mit help für die neuen befehle auch 1.1.2



#user können voicechannels erstellen

# jeder befehl kann in der config geändert werden genauso wie auch die permission node
#music bot

from modules import tempChannels, cmdChannel, tools, help, nicksystem
from modules import BigmacBansystem as BB
from core import Permissions, config, user, log
import discord.client

version = '1.1.2'

configFile = 'config.ini'
config_obj = config.Main(configFile)
config_data = config_obj.get_config()

class Main(discord.Client):
    async def on_ready(self):

        log.log('Info', 'Main', 'Api version: {0}.{1}.{2}'.format(discord.version_info.major, discord.version_info.minor, discord.version_info.micro))
        log.log('Info', 'Main', 'Bot version: {0}'.format(version))
        log.log('Info', 'Main', 'Logged in as: {0}'.format(self.user))
        log.log('Info', 'Main', 'Latency: {0}ms'.format(str(self.latency * 1000).split('.')[0]))
        self.appInfo = await self.application_info()
        log.log('Info', 'Main', 'I\'m owned by: {0}'.format(self.appInfo.owner))

        self.config = config_data
        self.guild = self.guilds[0]
        self.db = user.Main(self.config.userdbFilename, self.guild)

        self.tempChan = tempChannels.Main(self.guild)
        for cat in self.config.TempCategorys:
            self.tempChan.add_category(cat[0], cat[1])

        self.cmdChan = cmdChannel.Main(self.guild, self.db, self.config.cmdCategory_id)

        self.BBansystem = BB.Main(self.guild, self.db)
        self.Perms = Permissions.Main(self.db)

        self.Nicksys = nicksystem.Main(self.db, self.guild)

        self.help = help.Main(self.config.BotPrefix)

        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Pornos | Ver. {0}'.format(version)))

        self.commands = {
            'nick': [True, self.Nicksys.cmd_nick, 'bot.nick'],
            'ban': [True, self.BBansystem.cmd_ban, 'bot.ban'],
            'pardon': [True, self.BBansystem.cmd_pardon, 'bot.pardon'],
            'reload': [True, self.db.reload_users, 'bot.reload'],
            'lvl': [True, self.Nicksys.cmd_lvl, 'bot.lvl']
        }
        self.loop.create_task(self.Nicksys.test_members())
        log.log('Info', 'Main', 'Setup Completed...')

    async def on_message(self, message):
        check_result = self.BBansystem.test_member(str(message.author.id), 'tc')
        if check_result[0] == True:
            await message.delete()
            dm_channel = await message.author.create_dm()
            await dm_channel.send(check_result[1])

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
            if check_result[0] == True:
                await member.edit(voice_channel=None)
                dm_channel = await member.create_dm()
                await dm_channel.send(check_result[1])

        if self.config.TempChannels:
            await self.tempChan.voicechannel_update()

    async def on_member_join(self, member):
        self.db.add_user(member)

    async def on_member_remove(self, member):
        self.db.remove_user(member)

    async def on_user_update(self, before, after):
        self.db.update_user(after)

    async def channel_commands(self, message):
        cmd = message.content.split(' ')
        if cmd[0] == 'help':
            await self.help.cmd_help(message, cmd)
        else:
            try:
                if self.Perms.test_user(message.author.id, self.commands[cmd[0]][2]):
                    if self.commands[cmd[0]][0]: await self.commands[cmd[0]][1](message, cmd, self.guild, self.db)
                    else: await message.channel.send('Entschuldigung aber dieser Command ist Deaktiviert')
                else:
                    await message.channel.send('Du hast keine Rechte um diesem Command auszuführen')
            except KeyError:
                await message.channel.send('Diesen Command gibt es nicht für hilfe **"!help"**')

intents = discord.Intents(messages=True, guilds=True, members=True, voice_states=True)
bot = Main(intents=intents)
bot.run(config_data.BotSecret)
