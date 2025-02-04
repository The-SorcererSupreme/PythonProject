// src/app/services/container.service.ts
import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { isPlatformBrowser } from '@angular/common';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ContainerService {
  private apiUrl = 'http://localhost:8000/api/containers';  // Replace with your backend URL

  constructor(private http: HttpClient, @Inject(PLATFORM_ID) private platformId: Object) { }

  // Function to get containers for the current user
  getContainers(): Observable<any> {
    let headers = new HttpHeaders();

    // Check if we are in the browser environment
    if (isPlatformBrowser(this.platformId)) {
      console.log("Get Containers - It's a Browser!")
      const token = localStorage.getItem('auth_token');  // Retrieve the token from local storage (or session storage)
      if (token) {
        console.log("Get Containers - Token is set!")
        // Set headers with the JWT token if token exists
        headers = headers.set('Authorization', `Bearer ${token}`);
      }
    }

    // Now, you can make the request with the headers (which will be empty if not in the browser)
    return this.http.get(this.apiUrl, { headers });
  }
}
