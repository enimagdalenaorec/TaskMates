import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { InputNumberModule } from 'primeng/inputnumber';
import { SliderModule } from 'primeng/slider';
import { CalendarModule } from 'primeng/calendar';
import { ActivatedRoute } from '@angular/router';
import { PickerModule } from "@ctrl/ngx-emoji-mart";
import { NgIf } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-task',
  standalone: true,
  imports: [ReactiveFormsModule, InputTextModule, InputTextareaModule, InputNumberModule, SliderModule, CalendarModule, PickerModule, NgIf, HttpClientModule],
  templateUrl: './add-task.component.html',
  styleUrl: './add-task.component.css'
})
export class AddTaskComponent implements OnInit {
  addTaskForm: FormGroup;
  groupId: string = '';
  showEmojiPicker = false;
  message = '';
  icon = '';
  apiUrl = 'https://taskmatesbackend-pd5h.onrender.com/api'; // Django API endpoints
  today: Date = new Date();

  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {
    this.addTaskForm = new FormGroup({
      name: new FormControl('', Validators.required),
      description: new FormControl(''),
      capacity: new FormControl(1, Validators.required),
      points: new FormControl(100, Validators.required),
      deadline: new FormControl(new Date(), Validators.required),
      // icon: new FormControl('', Validators.required)
    });
  }

  ngOnInit(): void {
    this.addTaskForm.get('points')?.valueChanges.subscribe(value => {
      this.addTaskForm.get('points')?.setValue(value, { emitEvent: false });
    });
    this.groupId = this.route.snapshot.paramMap.get('group-id')!;
    // console.log('Group ID:', this.groupId);
  }

  addEmoji(event: any) {
    if (this.icon === '') {
      const { message } = this;
      this.icon = `${message}${event.emoji.native}`;
      this.showEmojiPicker = false;
    }
  }

  toggleVisability() {
    if (this.icon === '') {
    this.showEmojiPicker = !this.showEmojiPicker;
    }
  }

  handleKeydown(event: KeyboardEvent): void {
    if (event.key !== 'Backspace' && event.key !== 'Delete') {
      event.preventDefault();
    } else {
      this.icon = '';
    }
  }

  isFormDisabled(): boolean {
    return this.addTaskForm.invalid || this.icon === '';
  }

  onSubmit() {
    const body = {
      name: this.addTaskForm.value.name,
      description: this.addTaskForm.value.description,
      max_capacity: this.addTaskForm.value.capacity,
      points: this.addTaskForm.value.points,
      // deadline: this.addTaskForm.value.deadline.getFullYear() + '-' + this.increaseMonth(this.addTaskForm.value.deadline.getMonth()) + '-' + this.addTaskForm.value.deadline.getDate(),
      deadline: new Date(this.addTaskForm.value.deadline).toISOString(),
      icon: this.icon,
      groupId: this.groupId
    };
    // console.log('Task:', body);
    this.http.post(this.apiUrl + '/tasks/addTask', body).subscribe({
      next: (response) => {
        console.log(response);
        this.addTaskForm.reset();
        this.addTaskForm.patchValue({ capacity: 1, points: 100, deadline: new Date() });
        this.icon = '';
        this.router.navigate(['/group/' + this.groupId]);
      },
      error: (error) => {
        console.error('Error adding task:', error);
      }
    });
  }

  increaseMonth(number: number): number {     //not sure why i had to do this?
    return number + 1;
  }
}
