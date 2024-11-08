import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { BadgeModule } from 'primeng/badge';


@Component({
  selector: 'app-my-groups',
  standalone: true,
  imports: [CommonModule, FormsModule, InputTextModule, ButtonModule, CardModule, BadgeModule],
  templateUrl: './my-groups.component.html',
  styleUrl: './my-groups.component.css'
})
export class MyGroupsComponent {

  searchQuery='';
  groups = [
    { name: 'Roommates', hasNotification: true, hasChat: true },
    { name: 'Biology project', hasNotification: false, hasChat: false },
    { name: 'Parents house', hasNotification: false, hasChat: true },
    // Add more groups as needed
  ];
}
