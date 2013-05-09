#include <Windows.h>
#include "multask.h"
#include "tasker.h"

CRITICAL_SECTION malloc_cs;
CRITICAL_SECTION free_cs;

void multask_initTasker(){
	InitializeCriticalSection(&malloc_cs);
	InitializeCriticalSection(&free_cs);
}

void multask_unInitTasker(){
	LeaveCriticalSection(&malloc_cs);
	LeaveCriticalSection(&free_cs);
}


Tasker* multask_createTasker(char* group,int id,TaskFunction task_fun,TaskArgs args){
	Tasker* tasker=NULL;
	EnterCriticalSection(&malloc_cs);
	tasker=(Tasker*)malloc(sizeof(Tasker));
	LeaveCriticalSection(&malloc_cs);
	if(tasker!=NULL){
		tasker->group=group;
		tasker->id=id;
		tasker->task_fun=task_fun;
		tasker->args=args;
		tasker->is_finish=false;
		tasker->last=NULL;
		tasker->next=NULL;
	}
	return tasker;
}

void multask_freeTasker(Tasker* tasker){
	if(tasker!=NULL){
		EnterCriticalSection(&free_cs);
		free(tasker);
		LeaveCriticalSection(&free_cs);
	}
}