#coding=utf-8
__author__ = 'snower'

DEFAULT_SETTINGS={
    "default_worker":2,
    "max_worker":20,
    "manager_time":100,
    "worker_idle_time":100,
    "worker_busy_time":4,
    "event_type_cache_time":50,
    "debug":True
}

class Settings:
    settings=None
    def __init__(self,settings):
        """

        :param settings:
        """
        self.default()
        self.parseSettings(settings)

    def default(self):
        """


        """
        self.parseSettings(DEFAULT_SETTINGS)

    def parseSettings(self,settings):
        """

        :param settings:
        """
        for key in settings:
            if DEFAULT_SETTINGS.has_key(key):
                setattr(self,key,settings[key])

    def setSetting(self,name,setting):
        """

        :param name:
        :param setting:
        """
        setattr(self,name,setting)
