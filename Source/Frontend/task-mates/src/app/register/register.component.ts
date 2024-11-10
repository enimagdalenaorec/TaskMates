import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { FormControl, FormGroup, FormsModule, Validators } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { FloatLabelModule } from 'primeng/floatlabel';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { ReactiveFormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [InputTextModule, FloatLabelModule, PasswordModule, ButtonModule, ReactiveFormsModule, FormsModule, RouterModule, CommonModule, NgIf, HttpClientModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  email: string | undefined;
  password: string | undefined;
  repeatPassword: string | undefined;
  registerForm!: FormGroup;
  errorMessage: string | undefined;

  constructor(private router: Router, private http: HttpClient) { }

  ngOnInit() {
    this.registerForm = new FormGroup({
      Email: new FormControl<string>('', [Validators.required, Validators.email]),
      Password: new FormControl<string>('', Validators.required),
      RepeatPassword: new FormControl<string>('', Validators.required)
    });
  }

  onSubmit() {
    this.errorMessage = undefined;
    // check if the passwor and repeated password are the same
    // Call backend API to register
  }
}
