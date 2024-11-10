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
  imports: [FormsModule, ReactiveFormsModule, InputTextModule, PasswordModule, ButtonModule, RouterModule, NgIf, HttpClientModule],
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
    /*'http://localhost:8000/api/accounts/googleLogin' */
    window.location.href = 'http://localhost:8000/api/accounts/googleLogin/';
    // this.http.get('http://localhost:8000/api/accounts/googleLogin/').subscribe(
    //   response => {
    //     console.log(response);
    //   },
    //   error => {
    //     console.log(error);
    //   }
    // );

  }

  // signInWithGoogle() {
  //   this.http.get<{ url: string }>('http://localhost:8000/api/accounts/google/login').subscribe(
  //     response => {
  //       const googleSignInWindow = window.open(response.url, '_blank', 'width=500,height=600');
  //       const interval = setInterval(() => {
  //         if (googleSignInWindow && googleSignInWindow.closed) {
  //           clearInterval(interval);
  //           // Handle the token returned by the backend
  //           this.handleGoogleSignIn();
  //         }
  //       }, 1000);
  //     },
  //     error => {
  //       this.errorMessage = 'Failed to initiate Google sign-in process.';
  //     }
  //   );
  // }

  // handleGoogleSignIn() {
  //   // Call the backend to get the token after Google sign-in
  //   this.http.get<{ token: string }>('/api/auth/google/callback').subscribe(
  //     response => {
  //       const token = response.token;
  //       // Handle the token (e.g., save it, navigate to another page, etc.)
  //       console.log('Google sign-in token:', token);
  //       this.router.navigate(['/my-groups']);
  //     },
  //     error => {
  //       this.errorMessage = 'Failed to complete Google sign-in process.';
  //     }
  //   );
  // }
}
