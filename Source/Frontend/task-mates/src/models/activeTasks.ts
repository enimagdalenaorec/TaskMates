export interface Task {
    id: string;
    taskName: string;
    groupName: string;
    timeLeft: Date; 
    icon: string;
    points: number;
  }
  
  export class ActiveTasks {
    tasks: Task[]; 
  
    constructor(tasks: Task[] = []) {
      this.tasks = tasks; 
    }
  }
  