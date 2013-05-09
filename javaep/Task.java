package multask;

import multask.Tasker;
import multask.TaskerQueue;
import multask.WorkerQueue;

public class Task {
	private static TaskerQueue tasker_queue=null;
	private static WorkerQueue worker_queue=null;
	
	public Task(){
		this.init();
	}
	
	private void init(){
		this.tasker_queue=new TaskerQueue();
		this.worker_queue=new WorkerQueue();
	}
	
	public void loop(boolean sync){
		
	}
	
	public void exit(){
		this.worker_queue.exitAllWorker();
	}
	
	public static boolean postTasker(Tasker tasker){
		tasker_queue.push(tasker);
		worker_queue.wakeUpOneIdleWorker();
		return true;
	}
	
	public static boolean sendTasker(Tasker tasker){
		tasker.run();
		return true;
	}
	
	public static TaskerQueue getTaskerQueue(){
		return tasker_queue;
	}
	
	public static WorkerQueue getWorkerQueue(){
		return worker_queue;
	}
}
