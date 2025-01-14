import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { Feature1Component } from './components/feature1/feature1.component';
import { Feature2Component } from './components/feature2/feature2.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { AuthGuard } from './services/auth.guard'; // Import the guard

export const routes: Routes = [
  { path: '', component: HomeComponent, canActivate: [AuthGuard]},
  { path: 'feature1', component: Feature1Component, canActivate: [AuthGuard] },
  { path: 'feature2', component: Feature2Component, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
/*  { 
    path: 'login', 
    loadComponent: () => import('./login/login.component').then(m => m.LoginComponent), canActivate: [AuthGuard]
  },
  { 
    path: 'register', 
    loadComponent: () => import('./register/register.component').then(m => m.RegisterComponent), canActivate: [AuthGuard] 
  },*/
  // Optionally handle 404 (not found) routes
  { path: '**', redirectTo: 'login', pathMatch: 'full' },
];
