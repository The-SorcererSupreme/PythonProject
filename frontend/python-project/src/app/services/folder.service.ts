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
  fetchFileContent(path: string): Observable<any> {
    const url = `${this.baseUrl}/getFile?path=${encodeURIComponent(path)}`;
    console.log('Requesting file content URL:', url);  // Debug log for the file content request
    return timer(300).pipe(switchMap(() => this.http.get(url)));
  }
}
