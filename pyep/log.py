#coding=utf-8
__author__ = 'snower'

import traceback
from settings import Settings

class Log:
    log_self=None
    def __init__(self):
        """


        """
        self.settings=Settings.settings
        if self.settings.debug:
            self.out=Debug()
        else:
            self.out=Release()

    @staticmethod
    def initLog():
        """


        """
        Log.log_self=Log()

    @staticmethod
    def log(msg=""):
        """

        :param msg:
        """
        Log.log_self.out.output(msg)

    @staticmethod
    def waring(msg=""):
        """

        :param msg:
        """
        Log.log_self.out.waring(msg)

class Debug:
    def __init__(self):
        """


        """
        pass

    def output(self,msg):
        """

        :param msg:
        """
        print msg

    def waring(self,msg):
        """

        :param msg:
        """
        traceback.print_exc()
        self.output(msg)

class Release:
    def __init__(self):
        """


        """
        pass

    def output(self,msg):
        """

        :param msg:
        """
        print msg

    def waring(self,msg):
        """

        :param msg:
        """
        self.output(msg)