#ifndef _WORKER_H
#define _WORKER_H

#include <Windows.h>
#include <process.h>

#define multask_WORKER_STATUS_INITED 1
#define multask_WORKER_STATUS_IDLE 2
#define multask_WORKER_STATUS_BUSY 3
#define multask_WORKER_STATUS_ENDED 4

typedef INT8 WorkerStatus;

typedef struct Worker
{
	HANDLE thread;
	WorkerStatus status;
	bool is_stop;
	long status_change_time;
};

Worker* newWorker();
void deleteWorker(Worker* worker);
void initWorker(Worker* worker);
void changeStatus(Worker* worker,WorkerStatus status); 
unsigned int __stdcall run(void* param);

extern void multask_startWorker(Worker* worker);
extern void multask_stopWorker(Worker* worker);
extern void multask_wakeUpWorker(Worker* worker);
extern void multask_sleepWorker(Worker* worker);

extern DllExport Worker* multask_createWorker();
extern DllExport void multask_freeWorker(Worker* worker);

#endif