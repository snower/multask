#coding=utf-8
__author__ = 'snower'

from threading import currentThread
from threading import Thread
from threading import Condition
from threading import Lock
from log import Log
from settings import Settings
from event import Event

class WorkerExitError(StandardError):pass

class Worker(Thread):
    WOEKER_INIT=0
    WORKER_IDLE=1
    WORKER_BUSY=2
    WORKER_END=3
    def __init__(self,worker_manager):
        """

        :param worker_manager:
        """
        super(Worker,self).__init__()
        self.worker_manager=worker_manager
        self.condition=Condition()
        self.id=0
        self.is_stop=False
        self.status=Worker.WOEKER_INIT
        self.status_change_start=0
        self.task=None

    def init(self):
        """


        """
        self.id=self.ident

    def run(self):
        """


        """
        self.init()
        while True:
            if not self.task:
                self.changeStatus(Worker.WORKER_IDLE)
                self.sleepWorker()
                self.changeStatus(Worker.WORKER_BUSY)
            if self.task:
                try:
                    self.task(self)
                except WorkerExitError,e:
                    break
                except Exception,e:
                    Log.waring()
        self.changeStatus(Worker.WORKER_END)

    def stop(self):
        """


        """
        self.is_stop=True
        self.setTask(self.exit_task)
        self.wakeWorker()
        self.join()

    def changeStatus(self,status):
        """

        :param status:
        """
        self.status=status
        self.status_change_start=self.worker_manager.manager_count
        if self.status==Worker.WORKER_IDLE:
            self.worker_manager.worker_queue.pushIdle(self)
        elif self.status==Worker.WORKER_BUSY:
            self.worker_manager.worker_queue.popIdle(self)

    def getStatus(self):
        """


        :return:
        """
        return self.status

    def sleepWorker(self):
        """


        """
        self.condition.acquire()
        self.condition.wait()
        self.condition.release()

    def wakeWorker(self):
        """


        """
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def setTask(self,task):
        """

        :param task:
        """
        self.task=task

    def exit_task(self,worker):
        """

        :param worker:
        :raise:
        """
        print Log.log("Worker "+str(self.id)+" exit!")
        self.setTask(None)
        raise WorkerExitError()


class WorkerManager:
    def __init__(self,processor):
        """

        :param processor:
        """
        self.worker_queue=WorkerQueue()
        self.settings=Settings.settings
        self.processor=processor
        self.event_queue=processor.getEventQueue()
        self.is_stop=False
        self.manager_thread=None
        self.idle_start=0
        self.is_idle=True
        self.manager_count=0

    def init(self):
        """


        """
        self.manager_thread=currentThread()
        self.initDefaultWorker()

    def initDefaultWorker(self):
        """


        """
        for i in range(0,self.settings.default_worker):
            self.worker_queue.increaseWorker(self)

    def manager(self,manager_count):
        """

        :param manager_count:
        """
        self.manager_count=manager_count
        if not self.is_stop:
            event_queue_count=self.event_queue.count()
            if event_queue_count>self.settings.worker_busy_time*self.worker_queue.count():
                if self.worker_queue.count()<self.settings.max_worker:
                    self.worker_queue.increaseWorker(self)
            else:
                if self.worker_queue.count()>self.settings.default_worker:
                    self.worker_queue.decreaseWorker(manager_count)
                if event_queue_count<=0:
                    if not self.is_idle:
                        self.idle_start=manager_count
            self.is_idle=(self.event_queue.count()<=0)

    def stop(self):
        """


        """
        self.is_stop=True
        self.worker_queue.stopAllWorker()

    def wakeWorkerOfEvent(self,work_task):
        """

        :param work_task:
        """
        worker=self.worker_queue.popIdle()
        if worker:
            worker.setTask(work_task)
            worker.wakeWorker()

class WorkerQueue:
    def __init__(self):
        """


        """
        self.queue=[]
        self.idle_queue=[]
        self.settings=Settings.settings
        self.idle_lock=Lock()

    def increaseWorker(self,worker_manager):
        """

        :param worker_manager:
        """
        w=Worker(worker_manager)
        self.queue.append(w)
        w.start()

    def decreaseWorker(self,manager_count):
        """

        :param manager_count:
        """
        for q in self.queue:
            if q.status==Worker.WORKER_IDLE:
                if manager_count-q.status_change_start>self.settings.worker_idle_time*(self.count()-self.idleCount()+1):
                    q.stop()
                    self.queue.remove(q)
                    break

    def pushIdle(self,worker):
        """

        :param worker:
        """
        self.idle_lock.acquire()
        try:
            self.idle_queue.append(worker)
        except IndexError,e:
            self.idle_queue=self.idle_queue[:]
        self.idle_lock.release()

    def popIdle(self,worker=None):
        """

        :param worker:
        :return:
        """
        w=None
        self.idle_lock.acquire()
        if worker:
            try:
                self.idle_queue.pop(self.idle_queue.index(worker))
            except (ValueError,IndexError),e:
                pass
        else:
            try:
                w=self.idle_queue.pop()
            except IndexError,e:
                pass
        self.idle_lock.release()
        return w

    def count(self):
        """


        :return:
        """
        return len(self.queue)

    def idleCount(self):
        """


        :return:
        """
        c=0
        self.idle_lock.acquire()
        c=len(self.idle_queue)
        self.idle_lock.release()
        return c

    def stopAllWorker(self):
        """


        """
        for q in self.queue:
            q.stop()
        self.queue=[]

    def getWorkerById(self,id):
        """

        :param id:
        :return:
        """
        for q in self.queue:
            if q.id==id:
                return q