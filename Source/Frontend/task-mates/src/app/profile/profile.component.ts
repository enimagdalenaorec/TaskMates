import { NgFor, NgIf } from '@angular/common';
import { ActiveTasks } from './../../models/activeTasks';
import { Component , OnInit} from '@angular/core';
import { User, exampleProfilePicture } from '../../models/user';
import { Router } from '@angular/router';
import { Button } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';  // For PrimeNG Dialog
import { FormsModule } from '@angular/forms';  // Import FormsModule
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { profile } from 'node:console';


interface Task {
  id: number;
  taskName: string;
  groupName: string;
  timeLeft: { days: number; hours: number; minutes: number };
  icon: string;
  points: number;
};

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [NgFor, NgIf, Button, DialogModule, FormsModule, HttpClientModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css',
  providers: [MessageService],

})


export class ProfileComponent implements OnInit {
  activeTasks: any[] = []; // To hold the active tasks
  timeLeft: { [key: string]: { days: number, hours: number, minutes: number } } = {}; // Store time left for tasks
  profilePictureModalVisible = false;
  usernameModalVisible = false;
  newUsername = '';
  selectedFile: File | null = null;
  previewPicture: string | null = null;
  apiUrl = 'http://localhost:8000/api'; // Django API endpoints

  userInfo: any = {
    profilePicture: 'images/previewPicture.png',
    username: '',
    email: ''
  };

  editProfilePicture() {
    this.profilePictureModalVisible = true;
  }

  // Logic for handling file selection (profile picture)
  async onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
    this.previewPicture = await this.convertImageToBase64(this.selectedFile!); // Update the image in the modal
  }

  // Logic to save the new profile picture
  async saveProfilePicture() {
    if (this.selectedFile) {
      this.userInfo.profilePicture = await this.convertImageToBase64(this.selectedFile); // Update the image in the modal
       await this.changeProfilePicture(this.userInfo.profilePicture); // Save the new profile picture
      this.profilePictureModalVisible = false;
      // You can implement file upload logic here to save the image
    }
  }

  // Logic for opening modal to edit username
  editUsername() {
    this.usernameModalVisible = true;
  }

  // Logic to save the new username
  async saveUsername() {
    if (this.newUsername) {
      this.userInfo.username = this.newUsername;  // Update username
      await this.changeUsername();
      this.usernameModalVisible = false;
      // You can save the new username to your backend here
    }
  }

  constructor(
    private router: Router,
    private http: HttpClient,
    private messageService: MessageService
  ) { }

  ngOnInit(): void {
    this.previewPicture = 'images/previewPicture.png'; // Set the preview picture to the default profile picture
    this.fetchBasicUserInfo();
    this.fetchActiveTasks();
  }


  fetchActiveTasks(): void {
    this.http.get<{ tasks: Task[] }>(
      this.apiUrl + '/profile/get-active-tasks' // Adjust the endpoint if needed
    ).subscribe({
      next: (response) => {
        this.activeTasks = response.tasks || []; // Assign the tasks array
        // Calculate time left for each active task
        this.calculateTimeLeft();
      },
      error: (error) => {
        console.error('Error fetching active tasks:', error); // Updated error message
      }
    });
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


  private convertBase64ToImage(base64: string): string {
    return `data:image/jpg;base64,${base64}`;
  }

  convertImageToBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = error => reject(error);
    });
  }

  // Check if the task is active (you can modify this to suit your status logic)
  isActiveTask(task: Task): boolean {
    const timeLeft = task.timeLeft; // e.g., { days: 1, hours: 5, minutes: 30 }

        // Convert timeLeft to milliseconds
        const totalMilliseconds =
          (timeLeft.days || 0) * 24 * 60 * 60 * 1000 + // Days to ms
          (timeLeft.hours || 0) * 60 * 60 * 1000 + // Hours to ms
          (timeLeft.minutes || 0) * 60 * 1000; // Minutes to ms

        // Calculate the deadline as a Date
        const date = new Date(Date.now() + totalMilliseconds);

    return date > new Date(); // Consider tasks with a future deadline as active
  }
  navigateToTask(taskId: string): void {
    this.router.navigate(['/task', taskId]);
  }

  // Method to calculate time left for each active task
  calculateTimeLeft(): void {
    this.activeTasks.forEach(task => {
      const now = new Date();
      const deadline = new Date(now.getTime() + task.timeLeft * 1000); // Convert timeLeft from seconds to milliseconds
      const timeDiff = deadline.getTime() - now.getTime();

      if (timeDiff > 0) {
        const days = Math.floor(timeDiff / (1000 * 3600 * 24));
        const hours = Math.floor((timeDiff % (1000 * 3600 * 24)) / (1000 * 3600));
        const minutes = Math.floor((timeDiff % (1000 * 3600)) / (1000 * 60));

        this.timeLeft[task.id] = { days, hours, minutes };
      } else {
        this.timeLeft[task.id] = { days: 0, hours: 0, minutes: 0 };
      }
    });
  }

  changeUsername() {
    const body = {
      username: this.newUsername, // Assuming newUsername is a property of your component
    };

    this.http.post<any>(this.apiUrl + '/profile/change-username', body).subscribe({
      next: (response) => {
        // Handle success
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: response.message, // Show success message
        });
      },
      error: (error) => {
        // Handle error
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error?.message || 'Failed to change the username.', // Show error message
        });
      },
    });
  }

  changeProfilePicture(base64Image: string): void {
    const body = {
      profilePicture: base64Image,  // Send the Base64 image string in the request body
    };

    this.http.post<any>(`${this.apiUrl}/profile/change-profile-picture`, body).subscribe({
      next: (response) => {
        // Handle success
        
        this.fetchBasicUserInfo();
        this.profilePictureModalVisible = false; // Close the modal
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: response.message, // Show success message
        });
      },
      error: (error) => {
        // Handle error
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error?.message || 'Failed to change the profile picture.', // Show error message
        });
      },
    });
  }


  logout(): void {
    // Clear user session or navigate to login page
    this.http.get<any>(`${this.apiUrl}/accounts/logout`).subscribe({
      next: () => {
        console.log('Logged out successfully');
        this.router.navigate(['/login'])
      },
      error: (error) => {
        console.error('Logout failed', error);
      }
    });
    // Example: Navigate to login page
    // ;
  }

  // Handle task navigation (click)
  /* navigateToTask(taskId: string): void {
    console.log('Navigating to task with ID:', taskId);
    // Implement your navigation logic here
  } */
}
