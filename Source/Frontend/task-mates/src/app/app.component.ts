import { Component, OnInit, HostListener} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule, NgIf } from '@angular/common';
import { Router } from '@angular/router';
import { MenubarModule } from 'primeng/menubar';
import { ButtonModule } from 'primeng/button';
import { MenuItem } from 'primeng/api';
import { SidebarModule } from 'primeng/sidebar';
import { NotificationsComponent } from './notifications/notifications.component';
import { ProfileComponent } from './profile/profile.component';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { CalendarModule } from 'primeng/calendar';
import { HttpClient, HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, NgIf, MenubarModule, ButtonModule, SidebarModule, NotificationsComponent, ProfileComponent, CommonModule, CalendarModule, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'task-mates';
  items: MenuItem[] | undefined;
  sidebarVisible: boolean = true;

  isMobileOrTablet: boolean = false; // To track mobile or tablet screen size
  isHamburgerMenuVisible: boolean = false; // To control hamburger menu visibility
  isProfileIconClicked: boolean = false;
  tasksForCalendar: any[] = [];


  constructor(private router: Router,
    private breakpointObserver: BreakpointObserver, private http: HttpClient
  ) {
  }

  ngOnInit(): void {
    this.items = [
    ];

    // Subscribe to screen size changes (mobile, tablet, and desktop)
    this.breakpointObserver.observe([
      Breakpoints.XSmall,  // Mobile
      Breakpoints.Small,   // Small tablets
      Breakpoints.Medium,  // Medium devices, tablets, small laptops
      Breakpoints.Large    // Desktops
    ]).subscribe(result => {
      // Update the flag based on screen size (mobile or tablet = true)
      this.isMobileOrTablet = result.breakpoints[Breakpoints.XSmall] || result.breakpoints[Breakpoints.Small] || result.breakpoints[Breakpoints.Medium];

      // If on mobile or tablet, switch to hamburger menu
      if (this.isMobileOrTablet) {
        this.sidebarVisible = false;
        this.isHamburgerMenuVisible = true;
      } else {
        this.sidebarVisible = true;
        this.isHamburgerMenuVisible = false;
      }
    });

    this.http.get('http://localhost:8000/api/calendar/get-all-tasks').subscribe((data) => {
      this.tasksForCalendar = data as any[];
    }, (error) => {
      console.log(error);
    });
  }

  isHomeOrLoginOrRegisterRoute() {
    return this.router.url === '/' || this.router.url === '/login' || this.router.url === '/register' || this.router.url === '/home';
  }

  navigateTo(path: string) {
    this.router.navigate([path]);

    if (this.isMobileOrTablet) {
      this.toggleSidebar();
    }
  }
  isActive(path: string): boolean {
    return this.router.url.includes(path);
  }


    // Toggle the sidebar on mobile view
  toggleSidebar() {
    if (this.isProfileIconClicked != true) {
    this.sidebarVisible = !this.sidebarVisible;
    }
  }

}
