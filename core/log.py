import time
import os

class Logger:
    def __init__(self, filename_format):
        self.filename_format = filename_format

    #[20:28:32][Main\Info]: Hallo
    def log(self, lvl, fw, msg):
        output = '[{0}][{1}/{2}]: {3}'.format(time.strftime('%H:%M:%S'), fw, lvl, msg)
        self.write(output)
        print(output)

    #file_17-03-21.log
    def write(self, msg):
        filename = self.filename_format.format(time.strftime('%d-%m-%y'))
        file = open(filename, 'a', encoding='utf-8')
        file.write(msg + '\n')
        file.close()


logger = Logger('logs/LittleSteak_{0}.log')
log = logger.log