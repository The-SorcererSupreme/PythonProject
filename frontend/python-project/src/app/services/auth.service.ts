// auth.service.ts

import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';
import { jwtDecode } from "jwt-decode";

// Define the interface for the login response
interface LoginResponse {
  token: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private baseUrl = 'http://localhost:8000/auth'; // Replace with your backend URL

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
  login(username: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.baseUrl}/login`, { username, password });
  }

  // Store the JWT token (after login)
  saveSession(token: string): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem('auth_token', token); // Save token in localStorage
    }
  }

  // Retrieve the stored JWT token
  getToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem('auth_token');
    }
    return null; // On the server, return null
  }

  // Check if the user is logged in
  isLoggedIn(): boolean {
    const token = this.getToken();
    if (token) {
      try {
        const decoded: any = jwtDecode(token); // Decode the JWT token
        if (decoded.exp) {
          // Ensure 'exp' exists and check if it's greater than the current time
          return decoded.exp > Date.now() / 1000;
        }
      } catch (e) {
        console.error('Invalid token', e);
      }
    }
    return false; // Token doesn't exist or is invalid
  }

  // Logout the user (clear JWT token)
  logout(): void {
    const token = this.getToken();
    if (!token) {
      this.clearSession();
      return;
    }

    const headers = new HttpHeaders().set("Authorization", `Bearer ${token}`);

    this.http.post(`${this.baseUrl}/logout`, {}, { headers }).subscribe({
      next: () => {
        this.clearSession();
      },
      error: () => {
        this.clearSession(); // Ensure session is cleared even if API fails
      },
    });
  }

  // Method to get Authorization headers with JWT token
  getAuthHeaders(): HttpHeaders {
    const token = this.getToken();
    let headers = new HttpHeaders();
    if (token) {
      headers = headers.append('Authorization', `Bearer ${token}`); // Add token to Authorization header
    }
    return headers;
  }

  // Example of making a request with token
  makeAuthenticatedRequest(url: string): Observable<any> {
    const headers = this.getAuthHeaders();
    return this.http.get<any>(url, { headers });
  }

  clearSession(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem("auth_token");
    }
    this.router.navigate(["/login"]);
  }
}
