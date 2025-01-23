import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TaskService {
  private tasksSubject = new BehaviorSubject<any[]>([]);
  public tasks$ = this.tasksSubject.asObservable();  // Observable to subscribe to

  private apiUrl = 'https://taskmatesbackend-pd5h.onrender.com/api/calendar';

  constructor(private http: HttpClient) {}

  fetchTasksForCalendar() {
    this.http.get<{ tasks: any[] }>(`${this.apiUrl}/get-all-tasks`).subscribe({
      next: (data) => {
        this.tasksSubject.next(data.tasks); // Update the tasks list
      },
      error: (err) => {
        console.error('Error fetching tasks:', err);
      },
    });
  }
}
