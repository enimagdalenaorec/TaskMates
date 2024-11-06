import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'; // Standalone forms
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { RouterModule } from '@angular/router';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-create-group',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, InputTextModule, ButtonModule, RouterModule, NgIf],
  templateUrl: './create-group.component.html',
  styleUrl: './create-group.component.css'
})
export class CreateGroupComponent {
  groupName: string | undefined;
  errorMessage: string | undefined;
  createGroupForm!: FormGroup;

  constructor(private router: Router) { }

  ngOnInit() {
    this.createGroupForm = new FormGroup({
      GroupName: new FormControl('', Validators.required),
    });
  }

  onSubmit() {
    this.errorMessage = undefined;
    // Call API to login
  }
}
