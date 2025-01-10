// src/app/services/folder.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root', // Automatically makes it available across the app
})
export class FolderService {
  private apiUrl = 'http://127.0.0.1:5000/api/files'; // Adjust URL if needed

  constructor(private http: HttpClient) {}

  getFolderContents(path: string = ''): Observable<any> {
    const url = `${this.apiUrl}?path=${path}`;
    return this.http.get(url);
  }
}
