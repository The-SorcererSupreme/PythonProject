import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private baseUrl = 'http://localhost:5000/auth'; // Replace with your backend URL

  constructor(
    private http: HttpClient,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object // Inject PLATFORM_ID for SSR compatibility
  ) {}

  // Register a new user
  register(username: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/register`, { username, password });
  }

  // Login a user
  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/login`, { username, password });
  }

  // Store session after login (only on the client)
  saveSession(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem('userSession', 'true');
    }
  }

  // Check if the user is logged in (only on the client)
  isLoggedIn(): boolean {
    if (isPlatformBrowser(this.platformId)) {
      return !!localStorage.getItem('userSession');
    }
    return false; // On the server, assume the user is not logged in
  }

  // Logout the user (only on the client)
  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('userSession');
    }
    this.router.navigate(['/login']);
  }
}
