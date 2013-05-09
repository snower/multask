#ifndef TASKERQUEUE_H
#define TASKERQUEUE_H

void enterCriticalSection();

extern void multask_initTaskerQueue();
extern void multask_unInitTaskerQueue();

extern void multask_taskerPush(Tasker* tasker);

extern Tasker* multask_taskerPop();

extern long multask_taskerQueueCount();

#endif