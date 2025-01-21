import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { MyGroupsComponent } from './my-groups/my-groups.component';
import { ProfileComponent } from './profile/profile.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { CreateGroupComponent } from './create-group/create-group.component';
import { AddTaskComponent } from './add-task/add-task.component';
import { GroupComponent } from './group/group.component';
import { TaskComponent } from './task/task.component';
import { AuthGuardService } from './Services/AuthGuard/auth-guard.service';

export const routes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'home', component: HomeComponent},
  {path: 'login', component: LoginComponent},
  {path: 'my-groups', component: MyGroupsComponent, canActivate: [AuthGuardService]},
  {path: 'profile', component: ProfileComponent, canActivate: [AuthGuardService]},
  {path: 'notifications', component: NotificationsComponent, canActivate: [AuthGuardService]},
  {path: 'create-group', component: CreateGroupComponent, canActivate: [AuthGuardService]},
  {path: 'add-task/:group-id', component: AddTaskComponent, canActivate: [AuthGuardService]},
  { path: 'group/:id/:groupName', component: GroupComponent },
  {path: 'group/:id', component: GroupComponent},
  {path: 'task/:id', component: TaskComponent, canActivate: [AuthGuardService]},
  {path: '**', redirectTo: ''},
];
