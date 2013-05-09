package multask;

import multask.Tasker;

public class TaskerQueue {
	private class TaskerItem{
		public Tasker tasker=null;
		public TaskerItem last_tasker_item=null;
		public TaskerItem next_tasker_item=null;
		
		public TaskerItem(Tasker tasker){
			this.tasker=tasker;
		}
	}
	
	private TaskerItem tasker_queue_head=null;
	private TaskerItem tasker_queue_tail=null;
	private Object read_write_lock=null;
	private Object read_lock=null;
	private Object write_lock=null;
	private int count=0;
	
	public TaskerQueue(){
		this.tasker_queue_head=new TaskerItem(null);
		this.tasker_queue_tail=new TaskerItem(null);
		this.tasker_queue_head.next_tasker_item=this.tasker_queue_tail;
		this.tasker_queue_tail.last_tasker_item=this.tasker_queue_head;
		this.read_write_lock=new Object();
		this.read_lock=new Object();
		this.write_lock=new Object();
	}
	
	public void push(Tasker tasker){
		TaskerItem ti=new TaskerItem(tasker);
		this.tasker_queue_tail.last_tasker_item.next_tasker_item=ti;
		ti.last_tasker_item=this.tasker_queue_tail.last_tasker_item;
		this.tasker_queue_tail.last_tasker_item=ti;
		ti.next_tasker_item=this.tasker_queue_tail;
		this.count++;
	}
	
	public Tasker pop(){
		if(this.count<=0) return null;
		TaskerItem ti=this.tasker_queue_head.next_tasker_item;
		ti.next_tasker_item.last_tasker_item=this.tasker_queue_head;
		this.tasker_queue_head.next_tasker_item=ti.next_tasker_item;
		ti.last_tasker_item=null;
		ti.next_tasker_item=null;
		this.count--;
		return ti.tasker;
	}
	
	public int count(){
		return this.count;
	}
}
