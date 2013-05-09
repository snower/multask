package multask;

import multask.ITask;

public class Tasker {
	private String type=null;
	private int id=0;
	private ITask task=null;
	private Object[] args=null;
	
	public Tasker(String type){
		this.init(type, 0, null, null);
	}
	
	public Tasker(String type,int id){
		this.init(type, id, null, null);
	}
	
	public Tasker(String type,ITask task){
		this.init(type, 0, task, null);
	}
	
	public Tasker(String type,int id,ITask task){
		this.init(type, id, task, null);
	}
	
	public Tasker(String type,int id,ITask task,Object[] args){
		this.init(type, id, task, args);
	}
	
	private void init(String type,int id,ITask task,Object[] args){
		this.type=type;
		this.id=id;
		this.task=task;
		this.args=args;
	}
	
	public String getType(){
		return this.type;
	}
	
	public int getId(){
		return this.id;
	}
	
	public boolean run(){
		if(this.task==null) return false;
		return this.task.run(this.args);
	}
}
