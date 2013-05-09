#ifndef _TASK_H
#define _TASK_H

extern DllExport void multask_init();

extern DllExport void multask_loop();

extern DllExport void multask_exit();

extern DllExport bool multask_postTasker(Tasker* tasker);

extern DllExport bool multask_sendTasker(Tasker* tasker);

#endif