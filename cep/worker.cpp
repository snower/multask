#include "multask.h"
#include "worker.h"
#include "tasker.h"
#include "TaskerQueue.h"

Worker* newWorker(){
	Worker* worker=(Worker*)malloc(sizeof(Worker));
	if(worker!=NULL){
		worker->thread=NULL;
		worker->status=0;
		worker->is_stop=false;
		worker->status_change_time=0;
	}
	return worker;
}

void deleteWorker(Worker* worker){
	if(worker!=NULL){
		if(!(worker->is_stop==true && worker->status==multask_WORKER_STATUS_ENDED)){
			multask_stopWorker(worker);
		}
		free(worker);
	}
}

void initWorker(Worker* worker){
	if(worker!=NULL){
		worker->thread=NULL;
		worker->is_stop=false;
		changeStatus(worker,multask_WORKER_STATUS_INITED);
	}
}

void changeStatus(Worker* worker,WorkerStatus status){
	worker->status=status;
	worker->status_change_time=GetCurrentTime();
}

unsigned int __stdcall run(void* param){
	Worker* worker=(Worker*)param;
	Tasker* tasker=NULL;
	if(worker!=NULL){
		while (!worker->is_stop)
		{
			if((tasker=multask_taskerPop())==NULL){
				changeStatus(worker,multask_WORKER_STATUS_IDLE);
				multask_sleepWorker(worker);
			}
			else{
				changeStatus(worker,multask_WORKER_STATUS_BUSY);
				tasker->task_fun(tasker->args);
				tasker->is_finish=true;
				multask_freeTasker(tasker);
			}
		}
		changeStatus(worker,multask_WORKER_STATUS_ENDED);
		_endthreadex(0);
	}
	return 0;
}

void multask_startWorker(Worker* worker){
	if(worker!=NULL){
		if(worker->thread==NULL){
			worker->thread=(HANDLE)_beginthreadex(0,0,(unsigned int (__stdcall *)(void *))run,worker,0,0);
		}
	}
}

void multask_stopWorker(Worker* worker){
	if(worker!=NULL){
		worker->is_stop=true;
		while(worker->status!=multask_WORKER_STATUS_ENDED){
			if(worker->status==multask_WORKER_STATUS_IDLE){
				multask_wakeUpWorker(worker);
			}
		}
	}
}

void multask_wakeUpWorker(Worker* worker){
	if(worker!=NULL){
		if(worker->thread!=NULL && worker->status==multask_WORKER_STATUS_IDLE){
			ResumeThread(worker->thread);
		}
	}
}

void multask_sleepWorker(Worker* worker){
	if(worker!=NULL){
		if(worker->thread!=NULL && worker->status==multask_WORKER_STATUS_IDLE){
			SuspendThread(worker->thread);
		}
	}
}

Worker* multask_createWorker(){
	Worker* worker=newWorker();
	if(worker!=NULL){
		initWorker(worker);
	}
	return worker;
}

void multask_freeWorker(Worker* worker){
	deleteWorker(worker);
}