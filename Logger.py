import time
from datetime import datetime


class Logger:

    def __init__(self):
        self.log = 'log.txt'

    def log_line(self, line):
        with open(self.log, 'a+') as log:
            timestamp = datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
            log.write(f'{timestamp}: {line}\n')
            log.close()


if __name__ == '__main__':
    logger = Logger()
    logger.log_line('test')