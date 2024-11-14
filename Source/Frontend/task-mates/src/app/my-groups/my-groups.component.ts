import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { BadgeModule } from 'primeng/badge';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';


@Component({
  selector: 'app-my-groups',
  standalone: true,
  imports: [CommonModule, FormsModule, InputTextModule, ButtonModule, CardModule, BadgeModule, HttpClientModule],
  templateUrl: './my-groups.component.html',
  styleUrl: './my-groups.component.css'
})
export class MyGroupsComponent {

  cardImagePath = "images/group_images/picture1.jpg";
  searchQuery='';
  groups: any[] = [];  
  apiUrl = 'http://djangoTaskMates.onrender.com/api/groups/'; //TT Django API endpoint za render

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.fetchGroups();
  }

  fetchGroups(): void {
    this.http.get<{ groups: any[] }>(this.apiUrl).subscribe({
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
      this.http.post(this.apiUrl + "join", { code: this.searchQuery })
        .subscribe(
          (response) => {
            console.log('Successfully joined group:', response);
            this.fetchGroups();
            //this.router.navigate(['/group', response.id]);  Navigate to the group page (optional)
          },
          (error) => {
            console.error('Error joining group:', error);
          }
        );
    } else {
      console.log('Please enter a code in the search bar');
    }
  }

  navigateToGroup(groupId: string) {
    // Navigate to the group page, passing in the group ID
    this.router.navigate(['/group', groupId]);
  }
  
}
