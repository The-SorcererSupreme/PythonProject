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
  getContainers(includeShared: boolean = false): Observable<any> {
    let headers = new HttpHeaders();
    let url = this.apiUrl;

    // Check if we are in the browser environment
    if (isPlatformBrowser(this.platformId)) {
      console.log("Get Containers - It's a Browser!")
      const token = localStorage.getItem('auth_token');  
      if (token) {
        console.log("Get Containers - Token is set!")
        headers = headers.set('Authorization', `Bearer ${token}`);
      }
    }

    // Append query param if includeShared is true
    if (includeShared) {
      url += '?includeShared=true';
    }

    return this.http.get(url, { headers });
  }

  updateContainerName(containerId: string, newName: string): Observable<any> {
    let headers = new HttpHeaders();
  
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('auth_token');
      if (token) {
        headers = headers.set('Authorization', `Bearer ${token}`);
      }
    }
  
    return this.http.put(`${this.apiUrl}/update-name`, { id: containerId, name: newName }, { headers });
  }

    // Function to start a container
    startContainer(containerId: string): Observable<any> {
      let headers = new HttpHeaders();
  
      if (isPlatformBrowser(this.platformId)) {
        const token = localStorage.getItem('auth_token');
        if (token) {
          headers = headers.set('Authorization', `Bearer ${token}`);
        }
      }
  
      return this.http.post(`${this.apiUrl}/start`, { containerId }, { headers });
    }
  
    // Function to stop a container
    stopContainer(containerId: string): Observable<any> {
      let headers = new HttpHeaders();
  
      if (isPlatformBrowser(this.platformId)) {
        const token = localStorage.getItem('auth_token');
        if (token) {
          headers = headers.set('Authorization', `Bearer ${token}`);
        }
      }
  
      return this.http.post(`${this.apiUrl}/stop`, { containerId }, { headers });
    }
  
    deleteContainer(containerId: string): Observable<any> {
      let headers = new HttpHeaders();
    
      if (isPlatformBrowser(this.platformId)) {
        const token = localStorage.getItem('auth_token');
        if (token) {
          headers = headers.set('Authorization', `Bearer ${token}`);
        }
      }
    
      // Send the containerId in the body of the POST request
      return this.http.post(`${this.apiUrl}/delete`, { containerId }, { headers });
    }

      // Get users with access to a container
  getContainerAccess(containerId: string): Observable<any> {
    let headers = new HttpHeaders();
    
      if (isPlatformBrowser(this.platformId)) {
        const token = localStorage.getItem('auth_token');
        if (token) {
          headers = headers.set('Authorization', `Bearer ${token}`);
        }
      }
    return this.http.get<any>(`${this.apiUrl}/access?containerId=${containerId}`, { headers });
  }

  // Share a container with a new user
  shareContainer(containerId: string, username: string): Observable<any> {
    let headers = new HttpHeaders();
    
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('auth_token');
      if (token) {
        headers = headers.set('Authorization', `Bearer ${token}`);
      }
    }
    return this.http.post<any>(`${this.apiUrl}/share`, { containerId, username }, { headers });
  }

  // Revoke access for a user
  revokeAccess(containerId: string, userId: string): Observable<any> {
    let headers = new HttpHeaders();
    
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('auth_token');
      if (token) {
        headers = headers.set('Authorization', `Bearer ${token}`);
      }
    }
    return this.http.post<any>(`${this.apiUrl}/revoke`, { containerId, userId }, { headers });
  }

  // Method to trigger container export
  exportContainer(containerId: string): Observable<Blob> {
    let headers = new HttpHeaders();

    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('auth_token');
      if (token) {
        headers = headers.set('Authorization', `Bearer ${token}`);
      }
    }

    const url = `${this.apiUrl}/export`;  // Assuming export endpoint is here
    const body = { containerId };  // Send the containerId in the request body

    return this.http.post(url, body, { headers, responseType: 'blob' });
  }
}
