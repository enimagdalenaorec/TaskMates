import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { FormsModule, ReactiveFormsModule } from '@angular/forms'; // Standalone forms
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { RouterModule } from '@angular/router';
import { NgIf } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, ReactiveFormsModule, InputTextModule, PasswordModule, ButtonModule, RouterModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string | undefined;
  password: string | undefined;
  errorMessage: string | undefined;
  loginForm!: FormGroup;

  constructor(private router: Router, private http: HttpClient) { }

  ngOnInit() {
    this.loginForm = new FormGroup({
      Email: new FormControl('', Validators.required),
      Password: new FormControl('', Validators.required)
    });
  }

  onSubmit() {
    this.errorMessage = undefined;
    /*'https://taskmatesbackend-pd5h.onrender.com/api/accounts/googleLogin' */
    window.location.href = 'https://taskmatesbackend-pd5h.onrender.com/api/accounts/googleLogin/';
    // this.http.get('https://taskmatesbackend-pd5h.onrender.com/api/accounts/googleLogin/').subscribe(
    //   response => {
    //     console.log(response);
    //   },
    //   error => {
    //     console.log(error);
    //   }
    // );

  }

}
