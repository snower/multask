__author__ = 'sujian'

from time import sleep
import threading
from processor import Processor
from event import Event
from listener import Listener

processor=Processor({})

def listener(event,ba):
    if ba:
        print "listener type:",event.type,"before!",",worker_id:",threading.currentThread().id
    else:
        print "listener type:",event.type,"after!",",worker_id:",threading.currentThread().id

def event_fun(index):
    print "event_fun index:",index,",worker_id:",threading.currentThread().id
    for i in range(0,100000):
        pass

def exit_fun():
    in_str=raw_input("this test is end,you can press ENTER key exit or press R key repeat the test:")
    if in_str=="r" or in_str=="R":
        init()
    else:
        processor.exit()

def init():
    print "the test is start!"
    try:
        processor.registerListener(Listener("event_test",None,listener))
        for i in range(0,1000):
            processor.postEvent(Event("event_test",i,event_fun,(i,)))
        print "end"
        processor.postEvent(Event(type="event_exit",fun=exit_fun))
    except KeyboardInterrupt,e:
        processor.exit()

def main():
    print "this is processor test!"
    print "you can use CTRL+C exit test!"
    print "the test info:default worker:2,max_worker:20"
    sleep(3)
    processor.loop(False,init)
    print "test is ended!"
    print "time:",processor.manager_count*processor.settings.manager_time,"ms"

if __name__=="__main__":
    main()
