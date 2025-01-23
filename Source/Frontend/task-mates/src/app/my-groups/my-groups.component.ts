import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { BadgeModule } from 'primeng/badge';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';

interface Group {
  id: number;
  name: string;
  expiringSoonCount: number;
  unreadMessagesCount: number;
}

@Component({
  selector: 'app-my-groups',
  standalone: true,
  imports: [CommonModule, FormsModule, InputTextModule, ButtonModule, CardModule, BadgeModule, HttpClientModule],
  templateUrl: './my-groups.component.html',
  styleUrls: ['./my-groups.component.css']
})
export class MyGroupsComponent {

  searchQuery = '';
  groups: any[] = [];
  apiUrl = 'https://taskmatesbackend-pd5h.onrender.com/api/groups/'; // Django API endpoint



  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.fetchGroups();
  }

  fetchGroups(): void {
    this.http.get<{  groups: Group[]}>(this.apiUrl).subscribe({
      next: (response) => {
        this.groups = response.groups || [];
      },
      error: (error) => {
        console.error('Error fetching groups:', error);
      }
    });
  }

  navigateToCreateGroup() {
    this.router.navigate(['/create-group']);
  }

  joinGroup() {
    if (this.searchQuery.trim()) {
      this.http.post(this.apiUrl + "join", { code: this.searchQuery }, { withCredentials: true })
        .subscribe(
          (response) => {
            console.log('Successfully joined group:', response);
            this.fetchGroups();
            this.searchQuery = '';
            //this.router.navigate(['/group', response.id]);  // Navigacija na grupu (opcionalno)
          },
          (error) => {
            console.error('Error joining group:', error);
          }
        );
    } else {
      console.log('Please enter a code in the search bar');
    }
  }

  navigateToGroup(groupId: string, groupName: string) {
    const encodedGroupName = encodeURIComponent(groupName);
    this.router.navigate(['/group', groupId, encodedGroupName]);
  }
}
