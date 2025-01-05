import { NgFor, NgIf } from '@angular/common';
import { ActiveTasks, Task } from './../../models/activeTasks';
import { Component , OnInit} from '@angular/core';
import { User, exampleProfilePicture } from '../../models/user';
import { Router } from '@angular/router';
import { Button } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';  // For PrimeNG Dialog
import { FormsModule } from '@angular/forms';  // Import FormsModule
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';


@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [NgFor, NgIf, Button, DialogModule, FormsModule, HttpClientModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css',
  providers: [MessageService],

})

export class ProfileComponent implements OnInit {
  activeTasks: Task[] = []; // Store active tasks
  user: User=new User();
  timeLeft: { [key: string]: { days: number, hours: number, minutes: number } } = {}; // Store time left for tasks
  profilePictureModalVisible = false;
  usernameModalVisible = false;
  newUsername = '';
  selectedFile: File | null = null;
  apiUrl = 'http://127.0.0.1:8000/api'; // Django API endpoints


  
  editProfilePicture() {
    this.profilePictureModalVisible = true;
  }

  // Logic for handling file selection (profile picture)
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  // Logic to save the new profile picture
  saveProfilePicture() {
    if (this.selectedFile) {
      this.user.profilePicture = URL.createObjectURL(this.selectedFile); // Update the image in the modal
      this.profilePictureModalVisible = false;
      // You can implement file upload logic here to save the image
    }
  }

  // Logic for opening modal to edit username
  editUsername() {
    this.usernameModalVisible = true;
  }

  // Logic to save the new username
  saveUsername() {
    if (this.newUsername) {
      this.user.username = this.newUsername;  // Update username
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
    this.user.profilePicture = this.convertBase64ToImage(exampleProfilePicture);
    this.user.username = 'JohnDoe';
    this.user.email = 'johndoe@example.com';
    
    // Fetch or initialize tasks
    const exampleTasks: Task[] = this.getTasks();
    const activeTaskClass = new ActiveTasks(exampleTasks); // Instantiate ActiveTasks with fetched tasks

    // Filter only active tasks (you can customize this filtering logic)
    this.activeTasks = activeTaskClass.tasks ;

    // Calculate time left for each active task
    this.calculateTimeLeft();
  }

  // Example method to get tasks (replace with actual data fetching)
  getTasks(): Task[] {
    return [
      {
        id: '1',
        taskName: 'Complete Assignment',
        groupName: 'Group A',
        timeLeft: new Date('2024-06-30'),
        icon: '📝',
        points: 100,
      },
      {
        id: '2',
        taskName: 'Review PR',
        groupName: 'Group B',
        timeLeft: new Date('2024-07-01'),
        icon: '🔍',
        points: 50,
      },
      {
        id: '3',
        taskName: 'Write Blog Post',
        groupName: 'Group C',
        timeLeft: new Date('2024-07-05'),
        icon: '✍️',
        points: 80,
      },
    ];
  }
  private convertBase64ToImage(base64: string): string {
    return `data:image/jpg;base64,${base64}`;
  }

  // Check if the task is active (you can modify this to suit your status logic)
  isActiveTask(task: Task): boolean {
    return task.timeLeft > new Date(); // Consider tasks with a future deadline as active
  }
  navigateToTask(taskId: string): void {
    this.router.navigate(['/task', taskId]);
  }
  
  // Method to calculate time left for each active task
  calculateTimeLeft(): void {
    this.activeTasks.forEach(task => {
      const now = new Date();
      const deadline = new Date(task.timeLeft);
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
  
    this.http.post<any>(this.apiUrl + '/users/change-username', body).subscribe({
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

    this.http.post<any>(`${this.apiUrl}/users/change-profilePicture`, body).subscribe({
      next: (response) => {
        // Handle success
        this.user.profilePicture = base64Image; // Update the user profile picture
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
    console.log('User logged out');
    // Example: Navigate to login page
    // this.router.navigate(['/login']);
  }

  // Handle task navigation (click)
  /* navigateToTask(taskId: string): void {
    console.log('Navigating to task with ID:', taskId);
    // Implement your navigation logic here
  } */
}
