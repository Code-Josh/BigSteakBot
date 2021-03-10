import configparser

class Options:
    BotPrefix = '!'
    cmdChannelsFile = 'dbs/cmd_channels.json'
    bannedMembersFile = 'dbs/banned_members.json'
    permsFile = 'dbs/permissions.json'
    TempChannels = True
    CommandChannels = True
    createCMDChannel_id = 0
    cmdCategory_id = 0
    TempCategorys = []
    BotSecret = ''

class Main:
    def __init__(self, filename):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.options = []
        self.load_config()

    def get_config(self):
        self.options = Options()
        try:
            self.options.BotSecret = self.config['Core']['BotSecret']
            self.options.BotPrefix = self.config['Core']['BotPrefix']
            self.options.cmdChannelsFile = self.config['Files']['cmdChannelsFile']
            self.options.bannedMembersFile = self.config['Files']['bannedMembersFile']
            self.options.permsFile = self.config['Files']['permsFile']
            if self.config['Features']['TempChannels'] == 'True':
                self.options.TempChannels = True
            elif self.config['Features']['TempChannels'] == 'False':
                self.options.TempChannels = False
            else:
                print('Config Fehler!!!')

            self.options.cmdCategory_id = int(self.config['cmdChannel']['cmdCategory_id'])
            self.options.createCMDChannel_id = int(self.config['cmdChannel']['createCMDChannel_id'])

            self.options.CommandChannels = self.get_TempChannels()
            return self.options
        except KeyError:
            print('Config Error')

    def get_TempChannels(self):
        numCats = int(len(self.config['TempChannels']) / 2)
        tempchannels = []
        try:
            for i in range(1, numCats + 1):
                tempchannels.append([int(self.config['TempChannels']['Cat{0}_id'.format(i)]), self.config['TempChannels']['Cat{0}_format'.format(i)]])
            return tempchannels
        except ValueError:
            print('TempChannels Error!')


    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.filename, encoding='utf-8')