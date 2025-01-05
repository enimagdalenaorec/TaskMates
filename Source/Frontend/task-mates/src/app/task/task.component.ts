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

// Define an interface for the task member
interface TaskMember {
  name: string;
  picture: string;
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
    private http: HttpClient
  ) {}

  // Define the task type with members typed as TaskMember[]
  task: {
    id: number;
    name: string;
    groupName: string;
    members: TaskMember[];
    maxCapacity: number;
    currentCapacity: number;
    description: string;
    points: number;
    status: string;
    timeLeft: string;
    alreadyReviewed: boolean;
  } = {
    id: 1,
    name: 'Wash the dishes',
    groupName: 'Team Alpha',
    members: [
      {
        name: 'Alice',
        picture: `data:image/jpg;base64,${exampleProfilePicture}`,
      },
      {
        name: 'Bob',
        picture: `data:image/jpg;base64,${exampleProfilePicture}`,
      },
      {
        name: 'Alice',
        picture: `data:image/jpg;base64,${exampleProfilePicture}`,
      },
      {
        name: 'Bob',
        picture: `data:image/jpg;base64,${exampleProfilePicture}`,
      },
    ],
    maxCapacity: 5,
    currentCapacity: 2,
    description: 'Complete the Alpha project.',
    points: 150,
    status: 'available', // available | full | finished | failed
    timeLeft: '10d 15h 20m',
    alreadyReviewed: false,
  };

  isPerformingTask = false; // Check if user is part of the task
  rating = 0; // User's rating of the task
  visible: boolean = false;
  apiUrl = 'http://127.0.0.1:8000/api'; // Django API endpoints
  selectedFile: File | null = null;
  base64Image: string | null = null;

  get adjustedPoints(): number {
    if (this.task.status === 'failed' && this.isPerformingTask) {
      return this.task.points * 0.75; // Apply -25% if failed and performing task
    }
    return this.task.points; // Return original points if not failed or performing task
  }

  ngOnInit(): void {
    const loggedUser = 'Alic'; // Simulate logged-in user
    this.isPerformingTask = this.task.members.some(
      (member) => member.name === loggedUser
    );
    console.log(this.task.members);
  }

  showDialog() {
    this.visible = true;
  }

  saveReviewPicture() {
    if (!this.base64Image || !this.task.id) {
      this.messageService.add({
        severity: 'error',
        summary: 'Error',
        detail: 'Please select an image before submitting.',
      });
      return;
    }

    const body = {
      taskId: this.task.id,
      picture: this.base64Image.split(',')[1], // Remove the "data:image/png;base64," prefix
    };

    this.http.post(this.apiUrl + '/tasks/finish', body).subscribe({
      next: (response: any) => {
        this.messageService.add({ severity: 'success', summary: 'Success', detail: response.message });
        this.visible = false;
        this.task.status = 'finished'; // Update task status
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
    const body = {
      taskId: this.task.id, // Pass the taskId as part of the request body
    };

    this.http.post<any>(this.apiUrl + '/tasks/join', body).subscribe({
      next: (response) => {
        // Handle success
        this.task.currentCapacity++;
        this.isPerformingTask = true;

        if(this.task.currentCapacity >= this.task.maxCapacity){
          this.task.status = 'full';
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
      taskId: this.task.id, // Pass the taskId as part of the request body
    };

    this.http.post<any>(this.apiUrl + '/tasks/leave', body).subscribe({
      next: (response) => {
        // Handle success
        this.task.currentCapacity--;
        this.task.status = 'available';
        this.isPerformingTask = false;

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
      taskId: this.task.id, // Pass the taskId as part of the request body
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
        this.task.alreadyReviewed = true; // Mark task as reviewed
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
