#ifndef WORKERQUEUE_H
#define WORKERQUEUE_H

typedef struct WorkerItem
{
	WorkerItem* next;
	Worker* worker;
};

WorkerItem* newWorkerItem(Worker* w);
Worker* deleteWorkerItem(WorkerItem* wi);

void initDefaultWorker();
void increaseWorker();
void decreaseWorker();
void addWorker(Worker* worker);
Worker* removeWorker(Worker* worker);

extern void multask_initWorkerQueue();

extern void multask_unInitWorkerQueue();

extern void multask_wakeUpOneIdleWorker();

extern int multask_workerCount();

extern void multask_startAllWorker();

extern void multask_stopAllWorker();

#endif