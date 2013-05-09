package multask;

import java.util.Stack;
import java.util.LinkedList;
import multask.Settings;
import multask.Worker;

public class WorkerQueue {
	private LinkedList<Worker> worker_list=null;
	private Stack<Worker> idle_worker_list=null;
	
	public WorkerQueue(){
		this.worker_list=new LinkedList<Worker>();
		this.idle_worker_list=new Stack<Worker>();
		this.initDefaultWorker();
	}
	
	private void initDefaultWorker() {
		for(int i=0;i<Settings.Default_Worker;i++){
			this.increaseWorker();
		}
	}
	
	private void increaseWorker(){
		Worker worker=new Worker(this);
		this.worker_list.add(worker);
		this.idle_worker_list.push(worker);
		worker.start();
	}
	
	private void decreaseWorker(){
	}
	
	public void wakeUpOneIdleWorker(){
		if(!this.idle_worker_list.isEmpty()){
			Worker worker=this.idle_worker_list.pop();
			worker.wakeUpWorker();
		}
	}
	
	public void idleWorker(Worker worker){
		this.idle_worker_list.push(worker);
	}
	
	public void exitAllWorker(){
		for (Worker worker : this.worker_list) {
			worker.exit();
		}
	}
}
