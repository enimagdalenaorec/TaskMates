import { Component, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NgIf } from '@angular/common';
import { Router } from '@angular/router';
import { MenubarModule } from 'primeng/menubar';
import { ButtonModule } from 'primeng/button';
import { MenuItem } from 'primeng/api';
import { SidebarModule } from 'primeng/sidebar';
import { NotificationsComponent } from './notifications/notifications.component';
import { ProfileComponent } from './profile/profile.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NgIf, MenubarModule, ButtonModule, SidebarModule, NotificationsComponent, ProfileComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'task-mates';
  items: MenuItem[] | undefined;
  sidebarVisible: boolean = true;

  constructor(private router: Router) {
  }

  ngOnInit(): void {
    this.items = [
    ];
  }

  isHomeOrLoginOrRegisterRoute() {
    return this.router.url === '/' || this.router.url === '/login' || this.router.url === '/register' || this.router.url === '/home';
  }

  navigateTo(path: string) {
    this.router.navigate([path]);
  }
}
