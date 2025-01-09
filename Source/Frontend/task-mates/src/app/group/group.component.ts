import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Task } from '../../models/tasks';
import { TabViewModule } from 'primeng/tabview';
import { ButtonModule } from 'primeng/button';
import { TooltipModule } from 'primeng/tooltip';
import { interval, Subscription } from 'rxjs';
import { ApplicationRef } from '@angular/core';
import { first } from 'rxjs/operators';
import { NgZone } from '@angular/core';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { Member } from '../../models/members';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';

interface TimeLeft {
  days: number;
  hours: number;
  minutes: number;
}

@Component({
  selector: 'app-group',
  standalone: true,
  imports: [HttpClientModule, CommonModule, TabViewModule, ButtonModule, TooltipModule, OverlayPanelModule, DialogModule, InputTextModule],
  templateUrl: './group.component.html',
  styleUrl: './group.component.css'
})
export class GroupComponent implements OnInit {
  groupId: string = '';
  apiUrl = 'http://localhost:8000/api'; // Django API endpoints
  tasks: Task[] = [];
  groupName: string = '';
  private timerInterval: any;
  timeLeft: { [key: string]: TimeLeft } = {}; // Map with task ID as key and TimeLeft as value
  private timeUpdateSubscription: Subscription | null = null;
  filteredTasks: Task[] = [];
  members: Member[] = [];
  visible: boolean = false;
  groupCode: string = '';

  constructor(private router: Router, private route: ActivatedRoute, private http: HttpClient, private applicationRef: ApplicationRef, private ngZone: NgZone  ) {
  }


  ngOnInit(): void {
    this.groupId = this.route.snapshot.paramMap.get('id')!;
    this.groupName = this.route.snapshot.paramMap.get('groupName')!;
    this.fetchGroupTasksInfo();
    this.startTimerUpdates();
    this.fetchGroupMembers();
    this.fetchGroupLinkAndCode();
  }

  ngOnDestroy(): void {
    if (this.timeUpdateSubscription) {
      this.timeUpdateSubscription.unsubscribe();
    }
  }


  fetchGroupTasksInfo(): void {
    // Fetch group tasks info using the group ID
    this.http.post<{ tasks: any[] }>(this.apiUrl + '/tasks/getTasksByGroupId', { groupId: this.groupId }).subscribe({
      next: (response) => {
        this.tasks = response.tasks || [];
        //if not in url tak egroupName from first task
        if (this.groupName === '' || this.groupName === null) {
          this.groupName = this.tasks[0].groupName;
        }
        this.filteredTasks = this.tasks; // Display all tasks initially
        this.initializeTimeLeft();
        // console.log('Group tasks:', response.tasks);
      },
      error: (error) => {
        console.error('Error fetching group tasks:', error);
      }
    });
  }

  initializeTimeLeft(): void {
    this.tasks.forEach((task) => {
      this.timeLeft[task.id] = this.calculateTimeLeft(task.ts_deadline);
    });
  }

  calculateTimeLeft(deadline: string): TimeLeft {
    const deadlineDate = new Date(deadline);
    const now = new Date();
    const timeDiff = deadlineDate.getTime() - now.getTime();

    const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));

    return { days, hours, minutes };
  }

  startTimerUpdates(): void {
    this.applicationRef.isStable.pipe(first((isStable: boolean) => isStable)).subscribe(() => {
      // this.timeUpdateSubscription = interval(60000).subscribe(() => {
      //      this.updateAllTimeLeft();
      //      console.log('Timer updated');
      //    });
      this.ngZone.run(() => {
        setInterval(() => {
          this.updateAllTimeLeft();
          // console.log('Timer triggered');
        }, 60000);
      });
    });
  }

  updateAllTimeLeft(): void {
    for (const task of this.tasks) {
      this.timeLeft[task.id] = this.calculateTimeLeft(task.ts_deadline);
    }
  }

  isDeadlinePassed(deadline: string): boolean {
    const deadlineDate = new Date(deadline);
    const now = new Date();
    return now > deadlineDate;
  }

  filterTasks(status: string | null): void {
    if (status) {
      this.filteredTasks = this.tasks.filter((task) => task.status === status.toLowerCase());
    } else {
      this.filteredTasks = [...this.tasks];
    }
  }

  fetchGroupMembers(): void {
    this.http.post<{ members: any[] }>(this.apiUrl + '/groups/getAllMembers', { group_id: this.groupId }).subscribe({
      next: (response) => {
        this.members = response.members || [];
        // console.log('Group members:', response.members);
      },
      error: (error) => {
        console.error('Error fetching group members:', error);
      }
    });
  }

  showDialog() {
    this.visible = true;
}

copyToClipboard(text: string): void {
    navigator.clipboard.writeText(text).then(() => {
        // console.log('Group code copied to clipboard');
    });
}

fetchGroupLinkAndCode(): void {
    this.http.post<{ code: string, link: string }>(this.apiUrl + '/groups/getGroupCodeLink', { group_id: this.groupId }).subscribe({
      next: (response) => {
        this.groupCode = response.code;
      },
      error: (error) => {
        console.error('Error fetching group link and code:', error);
      }
    });
}

  navigate(location: string): void {
    this.router.navigate([location]);
  }

  navigateToTask(taskId: string): void {
    this.router.navigate(['/task', taskId]);
  }

  navigateToAddTask(): void {
    this.router.navigate(['/add-task', this.groupId]);
  }
}
