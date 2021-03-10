import discord

#Main Class für temporäre Channels
class Main:
    def __init__(self, guild):
        self.guild = guild
        self.TempChannelSettings = []

    def add_category(self, category_id, channel_format):
        category = self.guild.get_channel(category_id)
        if category != None and str(category.type) == 'category':
            self.TempChannelSettings.append([category, channel_format])
        elif category == None:
            print('Die Kategorie mit der id {0} wurde nicht gefunden'.format(category_id))
        elif str(category.type) != 'category':
            print('Der Channel mit der id {0} ist keine Kategorie'.format(category_id))

    async def voicechannel_update(self):
        for TempChannels in self.TempChannelSettings:
            VoiceChannels = []
            FullChannels = 0
            Channel_objs = []
            for channel in TempChannels[0].channels:
                if type(channel) == discord.channel.VoiceChannel:
                    Channel_objs.append(channel)
                    if len(channel.members) >= 1:
                        VoiceChannels.append(True)
                        FullChannels += 1
                    else:
                        VoiceChannels.append(False)
            if False not in VoiceChannels:
                await TempChannels[0].create_voice_channel(TempChannels[1].format(str(len(VoiceChannels) + 1)))
            if len(VoiceChannels) != 1 and VoiceChannels[-1] == False and FullChannels + 1 < len(VoiceChannels):
                await Channel_objs[-1].delete()