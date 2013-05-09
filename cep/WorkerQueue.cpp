#include "multask.h"
#include "worker.h"
#include "WorkerQueue.h"

WorkerItem* head;
int count;

WorkerItem* newWorkerItem(Worker* w){
	WorkerItem* wi=(WorkerItem*)malloc(sizeof(WorkerItem));
	if(wi!=NULL){
		wi->next=NULL;
		wi->worker=w;
	}
	return wi;
}

Worker* deleteWorkerItem(WorkerItem* wi){
	Worker* w=NULL;
	if(wi!=NULL){
		w=wi->worker;
		free(wi);
	}
	return w;
}

void initDefaultWorker(){
	int i=0;
	for(i=0;i<2;i++){
		increaseWorker();
	}
}

void increaseWorker(){
	Worker* w=multask_createWorker();
	addWorker(w);
}

void decreaseWorker(){
	Worker* w=head->next->worker;
	multask_stopWorker(w);
	w=removeWorker(w);
}

void addWorker(Worker* worker){
	WorkerItem* wi=newWorkerItem(worker);
	wi->next=head->next;
	head->next=wi;
	count++;
}

Worker* removeWorker(Worker* worker){
	int i=0;
	WorkerItem* wil=head;
	WorkerItem* wi=head->next;
	for(i=0;i<count;i++){
		if(wi->worker==worker){
			wil->next=wi->next;
			count--;
			return deleteWorkerItem(wi);
		}
		else{
			wi=wi->next;
		}
	}
	return NULL;
}

void multask_initWorkerQueue(){
	head=newWorkerItem(NULL);
	count=0;
	initDefaultWorker();
}

void multask_unInitWorkerQueue(){
	int i=0;
	for(i=0;i<count;i++){
		decreaseWorker();
	}
}

void multask_wakeUpOneIdleWorker(){
	int i=0;
	WorkerItem* wi=head->next;
	for(i=0;i<count;i++){
		if(wi->worker->status==multask_WORKER_STATUS_IDLE){
			multask_wakeUpWorker(wi->worker);
			break;
		}
	}
}

int multask_workerCount(){
	return count;
}

void multask_startAllWorker(){
	int i=0;
	WorkerItem* wi=head->next;
	for(i=0;i<count;i++){
		multask_startWorker(wi->worker);
		wi=wi->next;
	}
}

void multask_stopAllWorker(){
	int i=0;
	WorkerItem* wi=head->next;
	for(i=0;i<count;i++){
		multask_stopWorker(wi->worker);
		wi=wi->next;
	}
}