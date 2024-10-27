import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { MyGroupsComponent } from './my-groups/my-groups.component';
import { ProfileComponent } from './profile/profile.component';
import { NotificationsComponent } from './notifications/notifications.component';

export const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'home', component: HomeComponent},
  {path: 'login', component: LoginComponent},
  {path: 'my-groups', component: MyGroupsComponent},
  {path: 'profile', component: ProfileComponent},
  {path: 'notifications', component: NotificationsComponent}
];
