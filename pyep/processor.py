#coding=utf-8
__author__ = 'snower'
import threading
from time import sleep
from settings import Settings
from log import Log
from event import EventQueue
from event import Event
from worker import WorkerManager
from listener import ListenerManager
from listener import ListenerStopRunEventError

class ProcessorIsRunningError(StandardError):pass #Processor正在运行错误
class ProcessorNoRunningError(StandardError):pass #Processor未运行错误

class Processor:
    def __init__(self,settings={}):
        """
        :param settings:{}
        """
        Settings.settings=Settings(settings)
        self.settings=Settings.settings
        Log.initLog()
        self.event_queue=EventQueue()
        self.worker_manager=WorkerManager(self)
        self.listener_manager=ListenerManager(self)
        self.is_stop=True
        self.manager_count=0

    def loop(self,async=True,init=None):
        """
		启动入口函数
        :param async:bool
        :param init:Function
        :return:Thread :raise:ProcessorIsRunningError
        """
        if not self.is_stop:
            raise ProcessorIsRunningError()
        self.is_stop=False
        if async:
            t=threading.Thread(target=self.manager,args=(init,))
            t.start()
            return t
        else:
            self.manager(init)

    def manager(self,init=None):
        """
        :param init:Function
        """
        try:
            self.worker_manager.init()
            self.listener_manager.init()
            if init:init()
            while not self.is_stop:
                self.manager_count+=1
                try:
                    self.worker_manager.manager(self.manager_count)
                    self.listener_manager.manager(self.manager_count)
                    sleep(self.settings.manager_time/1000.00)
                except KeyboardInterrupt,e:
                    print "processor_exit:",KeyboardInterrupt
                    self.exit()
                    break
            self.worker_manager.stop()
        except Exception,e:
            from log import Log
            Log.waring()

    def getManagerCount(self):
        """
		返回管理器启动次数
        :return:int
        """
        return self.manager_count

    def work(self,worker):
        """

        :param worker:Worker
        :return:
        """
        event=self.event_queue.pop()
        if not event:
            worker.setTask(None)
            return
        self.runEvent(event)

    def runEvent(self,event):
        """
		运行event
        :param event:Event
        """
        try:
            self.listener_manager.listener(event,True)
            if event.fun:
                event.fun(*event.args)
            self.listener_manager.listener(event,False)
        except ListenerStopRunEventError,e:
            pass

    def exit(self):
        """
		退出
        :raise:ProcessorNoRunningError
        """
        if self.is_stop:
            raise ProcessorNoRunningError
        self.is_stop=True

    def postEvent(self,event):
        """
		以异步方式发送Event
        :param event:Event
        :return:bool
        """
        if self.is_stop:
            return False
        self.event_queue.push(event)
        self.worker_manager.wakeWorkerOfEvent(self.work)
        return True

    def sendEvent(self,event):
        """
		以同步方式发送Event
        :param event:Event
        :return:bool
        """
        if self.is_stop:
            return False
        self.runEvent(event)
        return True

    def getEventQueue(self):
        """
		返回Event队列
        :return:EventQueue
        """
        return self.event_queue

    def registerListener(self,listener):
        """
		注册event监听器
        :param listener:Listener
        """
        self.listener_manager.registerListener(listener)

    def unRegisterListener(self,listener):
        """
		取消注册event监听器
        :param listener:Listener
        """
        self.listener_manager.unRegisterListener(listener)
