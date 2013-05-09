#coding=utf-8
__author__ = 'snower'
from threading import Lock

class NoEventError(StandardError):pass

class Event:
    def __init__(self,type,id=None,fun=None,args=()):
        """

        :param type:
        :param id:
        :param fun:
        :param args:
        """
        self.type=type
        self.id=id
        self.fun=fun
        self.args=args

class EventQueue:
    def __init__(self):
        """


        """
        self.queue=[]
        self.lock=Lock()

    def push(self,event):
        """

        :param event:
        """
        self.lock.acquire()
        self.queue.append(event)
        self.lock.release()

    def pop(self):
        """


        :return:
        """
        event=None
        self.lock.acquire()
        try:
            event=self.queue.pop(0)
        except IndexError,e:
            event=None
        self.lock.release()
        return event

    def count(self):
        """


        :return:
        """
        self.lock.acquire()
        l=len(self.queue)
        self.lock.release()
        return l

    def clear(self):
        """


        """
        self.lock.acquire()
        self.queue=[]
        self.lock.release()