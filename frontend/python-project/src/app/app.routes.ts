import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { FileContentComponent } from './components/file-content/file-content.component';
import { FileUploadService } from './services/file-upload.service';
import { ContainersComponent } from './components/containers/containers.component';
import { AuthGuard } from './services/auth.guard'; // Import the guard
import { ContainerManagerComponent } from './components/container-manager/container-manager.component';
import { SettingsComponent } from './components/settings/settings.component';

export const routes: Routes = [
  { path: '', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'mngContainers', component: ContainerManagerComponent, canActivate: [AuthGuard] },
  { path: 'settings', component: SettingsComponent, canActivate: [AuthGuard] },
  { path: 'api/getFile', component: FileContentComponent, canActivate: [AuthGuard] },
  { path: 'api/upload', component: FileUploadService, canActivate: [AuthGuard] },
  { path: 'containers', component: ContainersComponent, canActivate: [AuthGuard] },

  // Allow access to authentication routes without AuthGuard
  { path: 'auth/login', component: LoginComponent },
  { path: 'auth/register', component: RegisterComponent },

  // Redirect all unknown routes to login
  { path: '**', redirectTo: 'auth/login', pathMatch: 'full' },
];