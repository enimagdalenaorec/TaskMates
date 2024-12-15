import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { InputNumberModule } from 'primeng/inputnumber';
import { SliderModule } from 'primeng/slider';
import { CalendarModule } from 'primeng/calendar';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-add-task',
  standalone: true,
  imports: [ReactiveFormsModule, InputTextModule, InputTextareaModule, InputNumberModule, SliderModule, CalendarModule],
  templateUrl: './add-task.component.html',
  styleUrl: './add-task.component.css'
})
export class AddTaskComponent implements OnInit {
  addTaskForm: FormGroup;
  groupId: string = '';

  constructor(private route: ActivatedRoute) {
    this.addTaskForm = new FormGroup({
      name: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
      capacity: new FormControl(1, Validators.required),
      points: new FormControl(100, Validators.required),
      deadline: new FormControl(new Date(), Validators.required)
    });
  }

  ngOnInit(): void {
    this.addTaskForm.get('points')?.valueChanges.subscribe(value => {
      this.addTaskForm.get('points')?.setValue(value, { emitEvent: false });
    });
    this.groupId = this.route.snapshot.paramMap.get('group-id')!;
    console.log('Group ID:', this.groupId);
  }

  onSubmit() {}
}
