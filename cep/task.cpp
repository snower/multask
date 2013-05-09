#include "multask.h"
#include "tasker.h"
#include "TaskerQueue.h"
#include "worker.h"
#include "WorkerQueue.h"
#include "task.h"

void multask_init(){
	multask_initTaskerQueue();
	multask_initWorkerQueue();
}

void multask_loop(){
	multask_startAllWorker();
}

void multask_exit(){
	multask_stopAllWorker();
	multask_unInitTaskerQueue();
	multask_unInitWorkerQueue();
}

bool multask_postTasker(Tasker* tasker){
	multask_taskerPush(tasker);
	multask_wakeUpOneIdleWorker();
	return false;
}

bool multask_sendTasker(Tasker* Tasker){
	return false;
}