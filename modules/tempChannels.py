import discord

#Main Class für temporäre Channels
class Main:
    def __init__(self, guild):
        self.guild = guild
        self.TempChannelSettings = []

    def add_category(self, category_name, channel_format):
        found = False
        for category in self.guild.categories:
            if category.name == category_name:
                found = True
                self.TempChannelSettings.append([category_name, channel_format, category])
        if not found:
            print('Die Kategorie {0} wurde nicht gefunden'.format(category_name))

    async def voicechannel_update(self):
        for TempChannels in self.TempChannelSettings:
            VoiceChannels = []
            FullChannels = 0
            Channel_objs = []
            for channel in TempChannels[2].channels:
                if type(channel) == discord.channel.VoiceChannel:
                    Channel_objs.append(channel)
                    if len(channel.members) >= 1:
                        VoiceChannels.append(True)
                        FullChannels += 1
                    else:
                        VoiceChannels.append(False)
            if False not in VoiceChannels:
                await TempChannels[2].create_voice_channel(TempChannels[1].format(str(len(VoiceChannels) + 1)))
            if len(VoiceChannels) != 1 and VoiceChannels[-1] == False and FullChannels + 1 < len(VoiceChannels):
                await Channel_objs[-1].delete()