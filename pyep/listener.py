#coding=utf-8
__author__ = 'snower'

import re
import threading
from settings import Settings

class ListenerStopRunEventError(StandardError):pass

class Listener:
    def __init__(self,etype,eid=None,fun=None):
        """

        :param etype:
        :param eid:
        :param fun:
        """
        self.event_type=etype
        self.event_id=eid
        self.fun=fun
        self.event_type_re=re.compile(self.event_type)
        if self.event_id:
            self.event_id_re=re.compile(self.event_id)
        else:
            self.event_id_re=None
        self.types=[]

class ListenerManager:
    def __init__(self,processor):
        """

        :param processor:
        """
        self.processor=processor
        self.settings=Settings.settings
        self.listener_list=ListenerList(processor)

    def init(self):
        """


        """
        pass

    def manager(self,manager_count):
        """

        :param manager_count:
        """
        types=self.listener_list.getTypeList()
        try:
            for t in types.keys():
                t=types[t]
                if manager_count-t.type_new>self.settings.event_type_cache_time and t.is_allow_remove:
                    self.listener_list.removeType(t.type)
        except KeyError,e:
            pass

    def isInitedType(self,type):
        """

        :param type:
        :return:
        """
        if not type:
            return
        if self.listener_list.hasType(type):
            return True
        return False

    def initType(self,type):
        """

        :param type:
        """
        if type:
            return self.listener_list.addType(type)

    def registerListener(self,listener):
        """

        :param listener:
        """
        self.listener_list.addListener(listener)

    def unRegisterListener(self,listener):
        """

        :param listener:
        """
        self.listener_list.removeListener(listener)

    def listener(self,event,ba):
        """

        :param event:
        :param ba:
        """
        ls=self.listener_list.getType(event.type)
        if not ls:
            ls=self.initType(event.type)
        for l in ls.listeners:
            if l.fun:
                if l.event_id_re:
                    if event.id:
                        if l.event_id_re.match(event.id):
                            l.fun(event,ba)
                else:
                    l.fun(event,ba)

class ListenerType:
    def __init__(self,type,is_allow_remove=True,type_start=0):
        """

        :param type:
        :param is_allow_remove:
        :param type_start:
        """
        self.type=type
        self.listeners=[]
        self.is_allow_remove=is_allow_remove
        self.type_start=type_start
        self.type_new=type_start

class ListenerList:
    def __init__(self,processor):
        """

        :param processor:
        """
        self.processor=processor
        self.listener_list=[]
        self.event_type_listeners={}
        self.lock=threading.Lock()

    def addListener(self,listener):
        """

        :param listener:
        """
        self.lock.acquire()
        self.listener_list.append(listener)
        self.listenerFindType(listener)
        self.lock.release()

    def removeListener(self,listener):
        """

        :param listener:
        """
        self.lock.acquire()
        self.listener_list.remove(listener)
        for t in listener.types:
            if self.event_type_listeners[t]:
                self.event_type_listeners[t].remove(listener)
        self.lock.release()

    def addType(self,type):
        """

        :param type:
        """
        self.lock.acquire()
        if not self.event_type_listeners.has_key(type):
            self.event_type_listeners[type]=ListenerType(type,True,self.processor.getManagerCount())
            self.typeFindListeners(type)
        self.lock.release()
        return self.event_type_listeners[type]

    def removeType(self,type):
        """

        :param type:
        """
        self.lock.acquire()
        ls=self.event_type_listeners.pop(type,None)
        if ls:
            for l in ls.listeners:
                l.types.remove(type)
        self.lock.release()
        return ls

    def typeFindListeners(self,type):
        """

        :param type:
        """
        for l in self.listener_list:
            if l.event_type_re.match(type):
                self.event_type_listeners[type].listeners.append(l)
                l.types.append(type)

    def listenerFindType(self,listener):
        """

        :param listener:
        """
        for t in self.event_type_listeners.keys():
            if listener.event_type_re.match(t):
                self.event_type_listeners[t].listeners.append(listener)
                listener.types.append(t)

    def getType(self,type):
        """

        :param type:
        :return:
        """
        if self.event_type_listeners.has_key(type):
            self.event_type_listeners[type].type_new=self.processor.getManagerCount()
            return self.event_type_listeners[type]
        return None

    def getTypeList(self):
        """


        :return:
        """
        return self.event_type_listeners

    def hasType(self,type):
        """

        :param type:
        :return:
        """
        return self.event_type_listeners.has_key(type)