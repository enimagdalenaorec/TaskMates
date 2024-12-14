import { Component, OnInit } from '@angular/core';
import { Notification } from '../../models/notifications';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import  { NgFor } from '@angular/common';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-notifications',
  standalone: true,
  imports: [HttpClientModule, NgFor, CommonModule],
  templateUrl: './notifications.component.html',
  styleUrl: './notifications.component.css'
})
export class NotificationsComponent implements OnInit {
  apiUrl = 'http://127.0.0.1:8000/api'; // Django API endpoints
  notifications: Notification[] = [];

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchNotifications();
  }

  fetchNotifications(): void {
    this.http.get<{notifications: any[]}>(`${this.apiUrl}/notifications/get-all`).subscribe((response) => {
      this.notifications = response.notifications;
    });
  }

}
