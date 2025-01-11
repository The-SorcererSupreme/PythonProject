// src/app/services/folder.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root', // Automatically makes it available across the app
})
export class FolderService {
  private baseUrl = 'http://localhost:5000/api/files'; // Update with your API URL

  constructor(private http: HttpClient) {}

  getFolderContents(path: string = ''): Observable<any> {
    const url = path ? `${this.baseUrl}?path=${path}` : this.baseUrl;
    return timer(300).pipe(switchMap(() => this.http.get(url))); // Add 300ms debounce
  }
}
