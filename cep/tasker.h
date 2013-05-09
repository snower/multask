#ifndef _TASKER_H
#define _TASKER_H

typedef void* TaskArgs;
typedef bool (*TaskFunction)(TaskArgs);

typedef struct Tasker
{
	char* group;
	int id;
	TaskFunction task_fun;
	TaskArgs args;
	bool is_finish;
	Tasker* last;
	Tasker* next;
};

extern void multask_initTasker();
extern void multask_unInitTasker();
extern DllExport Tasker* multask_createTasker(char* group,int id,TaskFunction task_fun,TaskArgs args);
extern DllExport void multask_freeTasker(Tasker* tasker);

#endif