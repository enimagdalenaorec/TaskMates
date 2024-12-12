import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Task } from '../../models/tasks';
import { TabViewModule } from 'primeng/tabview';
import { ButtonModule } from 'primeng/button';
import { TooltipModule } from 'primeng/tooltip';
@Component({
  selector: 'app-group',
  standalone: true,
  imports: [HttpClientModule, CommonModule, TabViewModule, ButtonModule, TooltipModule],
  templateUrl: './group.component.html',
  styleUrl: './group.component.css'
})
export class GroupComponent implements OnInit {
  groupId: string = '';
  apiUrl = 'http://127.0.0.1:8000/api'; // Django API endpoints
  tasks: Task[] = [];
  groupName: string = '';

  constructor(private router: Router, private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit(): void {
    this.groupId = this.route.snapshot.paramMap.get('id')!;
    this.fetchGroupTasksInfo();
  }

  fetchGroupTasksInfo(): void {
    // Fetch group tasks info using the group ID
    this.http.post<{ tasks: any[] }>(this.apiUrl + '/tasks/getTasksByGroupId', { group_id: this.groupId }).subscribe({
      next: (response) => {
        this.tasks = response.tasks || [];
        this.groupName = this.tasks[0].groupName;
        console.log('Group tasks:', response.tasks);
      },
      error: (error) => {
        console.error('Error fetching group tasks:', error);
      }
    });
  }

  navigate(location: string): void {
    this.router.navigate([location]);
  }
}
