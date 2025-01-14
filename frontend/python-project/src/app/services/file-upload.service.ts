// src/app/services/file-upload.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FileUploadService {

  private apiUrl = 'http://localhost:5000/api/upload';  // The URL where we will send the file to upload

  constructor(private http: HttpClient) {}

  uploadFiles(files: File[]): Observable<any> {
    const formData = new FormData();
    files.forEach(file => formData.append('file', file, file.name));

    return this.http.post(this.apiUrl, formData);
  }
}