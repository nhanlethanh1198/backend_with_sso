from enum import Enum
import logging
import os
from datetime import datetime


class AppLog:
    level = Enum('level',
                 {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR,
                  'critical': logging.CRITICAL})

    logger = None

    lvl = None

    def __init__(self, name):

        self.logger = logging.getLogger(name)

        self.logger.setLevel(logging.DEBUG)

        self.setLogHandle()

    def setLogHandle(self):
        log_filename = datetime.now().strftime('logs/%d_%m_%Y.log')

        fhandler = logging.FileHandler(log_filename, 'a', 'utf-8')

        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

        fhandler.setFormatter(formatter)

        fhandler.setLevel(logging.DEBUG)

        console = logging.StreamHandler()

        console.setFormatter(formatter)

        console.setLevel(logging.ERROR)

        self.logger.propagate = False

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(fhandler)

        self.logger.addHandler(console)

    def __getattr__(self, name):

        if (name in ('debug', 'info', 'warn', 'error', 'critical')):

            self.lvl = self.level[name].value

            return self

        else:

            raise AttributeError('Attr not Correct')

    def __call__(self, msg):

        self.logger.log(self.lvl, msg)
