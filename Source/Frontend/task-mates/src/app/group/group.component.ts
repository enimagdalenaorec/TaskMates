import { Component, OnInit, ApplicationRef, NgZone } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Task } from '../../models/tasks';
import { Member } from '../../models/members';
import { interval, Subscription, first, lastValueFrom } from 'rxjs';

import { TabViewModule } from 'primeng/tabview';
import { ButtonModule } from 'primeng/button';
import { TooltipModule } from 'primeng/tooltip';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { DialogModule } from 'primeng/dialog';
import { InputTextModule } from 'primeng/inputtext';

import { ChatClientService, ChannelService, StreamI18nService, StreamChatModule } from 'stream-chat-angular';
import { TranslateModule } from '@ngx-translate/core';

import { Secret } from '../../../secret';
import { textareaInjectionToken } from 'stream-chat-angular';
import { TextFieldModule } from '@angular/cdk/text-field';
import { CustomMessageInputComponent } from '../custom-message-input/custom-message-input.component';


interface TimeLeft {
  days: number;
  hours: number;
  minutes: number;
}

@Component({
  selector: 'app-group',
  standalone: true,
  imports: [
    HttpClientModule,
    CommonModule,
    TabViewModule,
    ButtonModule,
    TooltipModule,
    OverlayPanelModule,
    DialogModule,
    InputTextModule,
    StreamChatModule,
    TranslateModule,
    TextFieldModule
  ],
  providers: [
    { provide: textareaInjectionToken, useValue: CustomMessageInputComponent }
  ],
  templateUrl: './group.component.html',
  styleUrl: './group.component.css',
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
  userInfo: any = {
    profilePicture: null,
    username: '',
    email: '',
    id: ''
  };

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient,
    private applicationRef: ApplicationRef,
    private ngZone: NgZone,
    private chatService: ChatClientService,
    private channelService: ChannelService,
    private streamI18nService: StreamI18nService
  ) {
    // Ako želite odmah učitati prijevode
    this.streamI18nService.setTranslation();
  }

  async ngOnInit(): Promise<void> {

    const refreshRequired = localStorage.getItem('chatReloadRequired') === 'true';
     if (refreshRequired) {
    // The flag doesn't exist, trigger reload and set flag to 'true'
    localStorage.removeItem('chatReloadRequired');
    window.location.reload(); // Trigger page reload
    return; // Exit early to avoid the rest of the initialization
  }

   this.fetchBasicUserInfo();
   await new Promise(resolve => setTimeout(resolve, 100));
    // 1) Dohvat parametara iz URL-a
    this.groupId = this.route.snapshot.paramMap.get('id')!;
    this.groupName = decodeURIComponent(this.route.snapshot.paramMap.get('groupName')!);
    console.log('Group name:', this.groupName);

    // 2) Fetch osnovnih podataka (tasks, members, link i sl.)
    this.fetchGroupTasksInfo();
    this.startTimerUpdates();
    this.fetchGroupMembers();
    this.fetchGroupLinkAndCode();

    // 3) Dohvati chat token, pa inicijaliziraj klijenta
    const apiKey = new Secret().apiKey;
    const userId = this.userInfo.id.toString();
    try {
      const tokenResponse = await lastValueFrom(
        this.http.get<{ token: string }>('http://localhost:8000/api/groups/get_token')
      );
      const userToken = tokenResponse.token;
      console.log('User token:', userToken);

      await this.chatService.init(apiKey, { id: userId }, userToken);
      console.log('Chat client init done.');

      await this.chatService.chatClient.connectUser(
        {
          id: userId,
          name: this.userInfo.username
        },
        userToken
      );

      // 4) Tek sad možemo kreirati kanal (chatClient više nije undefined)
      const channel = this.chatService.chatClient.channel('messaging', this.groupId, {
        name: this.groupName,
        members:
            this.members.map((m) => m.userId.toString())
        ,
      });
      await channel.create();
      console.log('Channel created:', channel);

      // 5) Podesimo channelService za <stream-channel-list> ili <stream-channel> da zna koje kanale pretražiti
      this.channelService.init({
        type: 'messaging',
        id: { $eq: this.groupId },
      });
      console.log('ChannelService initialized with filter for group:', this.groupId);

      localStorage.setItem('chatReloadRequired', 'true');

    } catch (error) {
      console.error('Error fetching token or initializing chat client:', error);
    }

    this.fetchLeaderboardUrl();
  }

  ngOnDestroy(): void {
    if (this.timeUpdateSubscription) {
      this.timeUpdateSubscription.unsubscribe();
    }
  }

  fetchLeaderboardUrl(): void {
    this.http
      .post<{ url: string }>(this.apiUrl + '/groups/show_scoreboards', { group_id: this.groupId })
      .subscribe({
        next: (response) => {
          console.log('Leaderboard URL:', response.url);
        },
        error: (error) => {
          console.error('Error fetching leaderboard URL:', error);
        },
      });
  }

  fetchGroupTasksInfo(): void {
    this.http
      .post<{ tasks: any[] }>(this.apiUrl + '/tasks/getTasksByGroupId', { groupId: this.groupId })
      .subscribe({
        next: (response) => {
          this.tasks = response.tasks || [];
          // Ako parametar u URL-u nije dobar, uzmemo ime iz prvog taska
          if (
            this.groupName === 'null' ||
            this.groupName === '' ||
            this.groupName === 'undefined'
          ) {
            this.groupName = this.tasks[0]?.groupName || '';
          }
          this.filteredTasks = this.tasks;
          this.initializeTimeLeft();
        },
        error: (error) => {
          console.error('Error fetching group tasks:', error);
        },
      });
  }

  fetchGroupMembers(): void {
    this.http
      .post<{ members: any[] }>(this.apiUrl + '/groups/getAllMembers', { group_id: this.groupId })
      .subscribe({
        next: (response) => {
          this.members = response.members || [];
          console.log('Group members:', this.members);
        },
        error: (error) => {
          console.error('Error fetching group members:', error);
        },
      });
  }

  fetchGroupLinkAndCode(): void {
    this.http
      .post<{ code: string; link: string }>(this.apiUrl + '/groups/getGroupCodeLink', { group_id: this.groupId })
      .subscribe({
        next: (response) => {
          this.groupCode = response.code;
        },
        error: (error) => {
          console.error('Error fetching group link and code:', error);
        },
      });
  }

  // ========== Timer i deadline logika ==========

  startTimerUpdates(): void {
    this.applicationRef.isStable.pipe(first((isStable: boolean) => isStable)).subscribe(() => {
      this.ngZone.run(() => {
        setInterval(() => {
          this.updateAllTimeLeft();
        }, 60000);
      });
    });
  }

  initializeTimeLeft(): void {
    this.tasks.forEach((task) => {
      this.timeLeft[task.id] = this.calculateTimeLeft(task.ts_deadline);
    });
  }

  updateAllTimeLeft(): void {
    for (const task of this.tasks) {
      this.timeLeft[task.id] = this.calculateTimeLeft(task.ts_deadline);
    }
  }

  calculateTimeLeft(deadline: string): TimeLeft {
    const deadlineDate = new Date(deadline);
    const now = new Date();
    const timeDiff = deadlineDate.getTime() - now.getTime();

    const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
      (timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
    return { days, hours, minutes };
  }

  isDeadlinePassed(deadline: string): boolean {
    const deadlineDate = new Date(deadline);
    const now = new Date();
    return now > deadlineDate;
  }

  filterTasks(status: string | null): void {
    if (status) {
      this.filteredTasks = this.tasks.filter(
        (task) => task.status === status.toLowerCase()
      );
    } else {
      this.filteredTasks = [...this.tasks];
    }
  }

  // ========== Ostale metode ==========

  leaveGroup(): void {
    this.http
      .post<{ members: any[] }>(`${this.apiUrl}/groups/leave`, {
        groupId: this.groupId,
      })
      .subscribe({
        next: (response) => {
          console.log('Successfully left the group. Updated members:', response.members);
          this.fetchGroupMembers();
          this.router.navigate(['/my-groups']);
        },
        error: (error) => {
          console.error('Error leaving the group:', error);
        },
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

  navigate(location: string): void {
    this.router.navigate([location]);
  }

  navigateToTask(taskId: string): void {
    this.router.navigate(['/task', taskId]);
  }

  navigateToAddTask(): void {
    this.router.navigate(['/add-task', this.groupId]);
  }

  fetchBasicUserInfo(): void {
    this.http.get<{ profilePicture: string | null; username: string; email: string }>(
      this.apiUrl + '/profile/get-basic-info'
    ).subscribe({
      next: (response) => {
        this.userInfo = response; // Assign the entire response object
      },
      error: (error) => {
        console.error('Error fetching user info:', error);
      }
    });
  }
}
