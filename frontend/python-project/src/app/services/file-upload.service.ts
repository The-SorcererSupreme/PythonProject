// src/app/services/file-upload.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FileUploadService {

  private apiUrl = 'http://127.0.0.1:8000/api/upload';  // The URL where we will send the file to upload

  constructor(private http: HttpClient) {}

  uploadFiles(files: File[], uploadType: string = 'drag_and_drop'): Observable<any> {
    const formData = new FormData();
    files.forEach(file => formData.append('file', file, file.name));
    formData.append('upload_type', uploadType); // Add upload-type for use in fileupload_routes.py

    return this.http.post(this.apiUrl, formData);
  }
}