import { Component, OnInit } from '@angular/core';
import { NgIf, NgFor, CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Required for ngModel
import { Button } from 'primeng/button';
import { DataViewModule } from 'primeng/dataview';
import { Panel, PanelModule } from 'primeng/panel';
import { Knob, KnobModule } from 'primeng/knob';
import { User, exampleProfilePicture } from '../../models/user';
import { FileUpload, FileUploadModule } from 'primeng/fileupload';
import { Dialog, DialogModule } from 'primeng/dialog';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Rating, RatingModule } from 'primeng/rating';
import { SliderModule } from 'primeng/slider';
import { ActivatedRoute } from '@angular/router';

interface Member {
  name: string;
  picture: string | null;  // You can change this if you expect a URL or other data for the picture
}

interface Task {
  groupName: string;
  taskName: string;
  members: Member[];
  maxCapacity: number;
  currentCapacity: number;
  description: string;
  points: number;
  status: string;
  timeLeft: string;  // Time in seconds
  alreadyReviewed: boolean;
}


@Component({
  selector: 'app-task',
  standalone: true,
  imports: [
    Button,
    RatingModule,
    HttpClientModule,
    DialogModule,
    ToastModule,
    NgIf,
    FileUploadModule,
    FormsModule,
    DataViewModule,
    CommonModule,
    PanelModule,
    KnobModule,
    SliderModule
  ],
  templateUrl: './task.component.html',
  styleUrl: './task.component.css',
  providers: [MessageService],
  schemas: [CUSTOM_ELEMENTS_SCHEMA], // Optional, generally not needed
})
export class TaskComponent implements OnInit {
  constructor(
    private messageService: MessageService,
    private http: HttpClient,
    private route: ActivatedRoute     // To access route parameters

  ) {}


  task: Task | null=null;  // Strongly typed task object
  errorMessage: string = '';
  taskId: number | null = null;  // Define taskId
  timeLeftString : string | null=null;

  loggedUsername: string | null=null;


  isPerformingTask = false; // Check if user is part of the task
  rating = 0; // User's rating of the task
  visible: boolean = false;
  apiUrl = 'http://localhost:8000/api'; // Django API endpoints
  selectedFile: File | null = null;
  base64Image: string | null = null;

  get adjustedPoints(): number {
    if (this.task?.status === 'failed' && this.isPerformingTask) {
      return this.task?.points * 0.75; // Apply -25% if failed and performing task
    }
    return Number(this.task?.points); // Return original points if not failed or performing task
  }

   ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.taskId = +params['id']; // The '+' converts the string to a number
      this.fetchTaskById(this.taskId);
    });

    this.fetchBasicUserInfo();
  }

  fetchBasicUserInfo(): void {
    this.http.get<{ profilePicture: string | null; username: string; email: string }>(
      this.apiUrl + '/profile/get-basic-info'
    ).subscribe({
      next: (response) => {
        this.loggedUsername = response.username; // Assign the entire response object
      },
      error: (error) => {
        console.error('Error fetching user info:', error);
      }
    });
  }

  fetchTaskById(taskId: number): void {
    this.http.post<{ groupName: string, taskName: string, members: any[], maxCapacity: number,
                    currentCapacity: number, description: string, points: number,
                    status: string, timeLeft: number, alreadyReviewed: boolean }>(
      this.apiUrl + '/tasks/getTasksById', { taskId })
      .subscribe({
        next: (response) => {
          // Assuming response data has the structure of the task properties
          this.task = {
            groupName: response.groupName,
            taskName: response.taskName,
            members: response.members,
            maxCapacity: response.maxCapacity,
            currentCapacity: response.currentCapacity,
            description: response.description,
            points: response.points,
            status: response.status,
            timeLeft: this.convertTimeToHumanReadable(response.timeLeft),  // Time remaining in seconds
            alreadyReviewed: response.alreadyReviewed
          } ;
          this.isPerformingTask =
          this.task?.members?.some((member: any) => member.name === this.loggedUsername) || false;

          console.log(this.isPerformingTask)
        },
        error: (error) => {
          console.error('Error fetching task by ID:', error);
          // You can further handle the error, e.g., display an error message to the user
        }
      });
  }

  convertTimeToHumanReadable(seconds: number): string {
    const days = Math.floor(seconds / (3600 * 24));
    const hours = Math.floor((seconds % (3600 * 24)) / 3600);
    const mins = Math.floor((seconds % 3600) / 60);

    let result = '';
    result += `${days}d `;
     result += `${hours}h `;
    result += `${mins}m `;

    return result.trim(); // Trim any trailing spaces
  }

  showDialog() {
    this.visible = true;
  }

  saveReviewPicture() {
    if (!this.base64Image ) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please select an image before submitting.',
      });
      return;
    }

    const body = {
      taskId: this.taskId,
      picture: this.base64Image.split(',')[1], // Remove the "data:image/png;base64," prefix
    };

    this.http.post(this.apiUrl + '/tasks/finish', body).subscribe({
      next: (response: any) => {
        this.messageService.add({ severity: 'success', summary: 'Success', detail: response.message });
        this.visible = false;
        if (this.task)this.task.status = 'finished'; // Update task status
      },
      error: (error) => {
        console.error('Error uploading picture:', error);
        this.messageService.add({ severity: 'error', summary: 'Error', detail: 'Failed to upload picture' });
      },
    });
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;

      // Validate file type (ensure it's an image)
      if (!file.type.startsWith('image/')) {
        this.messageService.add({
          severity: 'error',
          summary: 'Invalid File Type',
          detail: 'Please select an image file.',
        });
        return;
      }

      // Check file size (optional: 5MB max)
      const maxFileSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxFileSize) {
        this.messageService.add({
          severity: 'error',
          summary: 'File Too Large',
          detail: 'Please select a file smaller than 5MB.',
        });
        return;
      }

      const reader = new FileReader();
      reader.onload = () => {
        this.base64Image = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }

  // Function to handle the Join button click
  joinTask() {
    console.log('taskId before sending:', this.taskId); // Check value of taskId

    const body = {
      taskId: this.taskId, // Pass the taskId as part of the request body
    };


    this.http.post<any>(this.apiUrl + '/tasks/join', body).subscribe({
      next: (response) => {
        // Handle success
        if (this.task){
        this.task.currentCapacity++;
        this.isPerformingTask = true;

        this.fetchTaskById(Number(this.taskId));

        if(this.task.currentCapacity >= this.task.maxCapacity){
          this.task.status = 'full';
        }
      }
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
          detail: error?.message || 'Failed to join the task.', // Show error message
        });
      },
    });
  }

  exitTask() {
    const body = {
      taskId: this.taskId, // Pass the taskId as part of the request body
    };

    this.http.post<any>(this.apiUrl + '/tasks/leave', body).subscribe({
      next: (response) => {
        // Handle success
        if (this.task) {this.task.currentCapacity--;
        this.task.status = 'available';}
        this.isPerformingTask = false;
        this.fetchTaskById(Number(this.taskId));


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
          detail: error?.message || 'Failed to leave the task.', // Show error message
        });
      },
    });
  }

  submitReview() {
    if (this.rating === null || this.rating === undefined) {
      return; // Ensure rating is provided before submitting
    }

    const body = {
      taskId: this.taskId, // Pass the taskId as part of the request body
      value: this.rating, // Pass the rating value to the backend
    };

    this.http.post<any>(this.apiUrl + '/tasks/review', body).subscribe({
      next: (response) => {
        // Handle successful response
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: response.message, // Show success message
        });
        console.log('Review submitted successfully:', response);

        if (this.task) this.task.alreadyReviewed = true; // Mark task as reviewed
      },
      error: (error) => {
        // Handle error response
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: error?.message || 'Error submitting review', // Show error message
        });
        console.error('Error submitting review:', error);
      },
    });
  }
}
