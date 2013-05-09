#include <Windows.h>
#include "multask.h"
#include "tasker.h"
#include "taskerqueue.h"

CRITICAL_SECTION link_cs;
Tasker* head;
Tasker* tail;
long count;

void enterCriticalSection(){
	long time_s=GetCurrentTime();
	while (!TryEnterCriticalSection(&link_cs))
	{
		if(GetCurrentTime()-time_s>1){
			EnterCriticalSection(&link_cs);
			break;
		}
	}
}

void multask_initTaskerQueue(){
	multask_initTasker();
	InitializeCriticalSection(&link_cs);
	head=multask_createTasker("__tasker_queue_head__",0,NULL,NULL);
	tail=multask_createTasker("__tasker_queue_tail__",0,NULL,NULL);
	head->next=tail;
	tail->last=head;
	count=0;
}

void multask_unInitTaskerQueue(){
	Tasker* ti=head;
	Tasker* tit=NULL;
	while(ti->next!=NULL){
		tit=ti;
		ti=ti->next;
		multask_freeTasker(tit);
	}
	multask_unInitTasker();
	DeleteCriticalSection(&link_cs);
}

void multask_taskerPush(Tasker* tasker){
	enterCriticalSection();
	tasker->last=tail->last;
	tasker->next=tail;
	tail->last->next=tasker;
	tail->last=tasker;
	count++;
	LeaveCriticalSection(&link_cs);
}

Tasker* multask_taskerPop(){
	Tasker* t=NULL;
	enterCriticalSection();
	if(count>0){
		t=head->next;
		t->next->last=head;
		head->next=t->next;
		count--;
	}
	LeaveCriticalSection(&link_cs);
	if(t!=NULL){
		t->last=NULL;
		t->last=NULL;
	}
	return t;
}

long multask_taskerQueueCount(){
	return count;
}