package multask;

import java.lang.Thread;
import multask.WorkerQueue;
import multask.TaskerQueue;

public class Worker extends  Thread{
	public enum Status{
		INITED,IDLE,BUSY,ENDED
	};
	
	private WorkerQueue queue=null;
	private TaskerQueue tasker_queue=null;
	private Status status=null;
	private long change_status_time=0;
	private boolean stoped=false;
	private Object waiter=null;
	
	public Worker(WorkerQueue queue){
		this.queue=queue;
		this.tasker_queue=Task.getTaskerQueue();
		this.waiter=new Object();
		this.changeStatus(Status.INITED);
	}
	
	private void changeStatus(Status status){
		if(this.status==status) return;
		this.status=status;
		this.change_status_time=System.currentTimeMillis();
	}
	
	public void run(){
		Tasker tasker=null;
		while (!this.stoped) {
			try {
				if((tasker=this.tasker_queue.pop())==null){
					this.changeStatus(Status.IDLE);
					this.sleepWorker();
				}
				else{
					this.changeStatus(Status.BUSY);
					tasker.run();
				}
			}catch (Exception e) {
				// TODO: handle exception
				e.printStackTrace();
			}
		}
		this.changeStatus(Status.ENDED);
	}
	
	public void sleepWorker(){
		synchronized (this.waiter) {
			this.queue.idleWorker(this);
			try {
				this.waiter.wait();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	public void wakeUpWorker(){
		synchronized (this.waiter) {
			this.waiter.notifyAll();
		}
	}
	
	public void exit(){
		synchronized (this.waiter) {
			if(this.status==Status.IDLE){
				this.waiter.notifyAll();
			}
			this.stoped=true;
		}
		try {
			this.join();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public Status getStatus(){
		return this.status;
	}
	
	public long getChangeStatusTime(){
		return this.change_status_time;
	}
}
