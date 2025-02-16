import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root', // Automatically makes it available across the app
})
export class FolderService {
  private baseUrl = 'http://localhost:8000/api'; // Base URL for API

  constructor(private http: HttpClient,) {}


  // Method to get folder contents
  getFolderContents(path: string = ''): Observable<any> {
    const url = path ? `${this.baseUrl}/files?path=${encodeURIComponent(path)}` : `${this.baseUrl}/files`;
    console.log('Requesting URL:', url);  // Debug log for the folder contents request
    return timer(300).pipe(switchMap(() => this.http.get(url)));
  }

  // New method to fetch file content
  fetchFileContent(path: string, container_id: string): Observable<any> {
    const url = `${this.baseUrl}/getFile?containerID=${encodeURIComponent(container_id)}&path=${encodeURIComponent(path)}`;
    // Get the token from local storage or any other storage mechanism you use
    const token = localStorage.getItem('auth_token');  // Replace with your token storage method

    // Add the token to the HTTP request headers
    const headers = {
      'Authorization': `Bearer ${token}`,
    };

    console.log('Requesting URL:', url);  // Debug log for the folder contents request

    return timer(300).pipe(
      switchMap(() => 
      this.http.get(url, { headers })
    ));
  }
  saveFileContent(path: string, container_id: string, content: string): Observable<any> {
    const url = `${this.baseUrl}/saveFile?containerID=${encodeURIComponent(container_id)}&path=${encodeURIComponent(path)}`; // The actual API endpoint for saving the file
    const body = {
      content,
    };
    // Get the token from local storage or any other storage mechanism you use
    const token = localStorage.getItem('auth_token');  // Replace with your token storage method

    // Add the token to the HTTP request headers
    const headers = {
      'Authorization': `Bearer ${token}`,
    };

    console.log('Requesting URL:', url);
    return this.http.post<any>(url, body, { headers });
  }
}
