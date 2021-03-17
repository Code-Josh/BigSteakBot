import configparser
from core import log

class Options:
    BotPrefix = '!'
    userdbFilename = 'db/users.json'
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
            self.options.userdbFilename = self.config['Files']['userdbFilename']
            if self.config['Features']['TempChannels'] == 'True':
                self.options.TempChannels = True
            elif self.config['Features']['TempChannels'] == 'False':
                self.options.TempChannels = False
            else:
                log.log('Error', 'Config', 'ConfigError')

            self.options.cmdCategory_id = int(self.config['cmdChannel']['cmdCategory_id'])
            self.options.createCMDChannel_id = int(self.config['cmdChannel']['createCMDChannel_id'])

            self.options.TempCategorys = self.get_TempChannels()
            log.log('Info', 'Config', 'Finished loading Config')
            return self.options
        except KeyError:
            log.log('Error', 'Config', 'Couldnt Read File or couldnt find Config Key')

    def get_TempChannels(self):
        numCats = int(len(self.config['TempChannels']) / 2)
        tempchannels = []
        try:
            for i in range(1, numCats + 1):
                tempchannels.append([int(self.config['TempChannels']['Cat{0}_id'.format(i)]), self.config['TempChannels']['Cat{0}_format'.format(i)]])
            return tempchannels
        except ValueError:
            log.log('Error', 'Config', 'TempChannels Error!')


    def load_config(self):
        self.config = configparser.ConfigParser()
        if self.config.read(self.filename, encoding='utf-8') == []:
            log.log('Fatal Error', 'Config', 'Cannot Read File')