import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true, // Mark as a standalone component
  imports: [FormsModule, CommonModule, RouterLink], // Import necessary modules
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  login() {
    this.authService.login(this.username, this.password).subscribe({
      next: () => {
        this.authService.saveSession(); // Save session on successful login
        location.href = '/'; // Redirect to home
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Login failed';
      },
    });
  }
}
