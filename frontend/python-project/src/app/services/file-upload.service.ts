// src/app/services/file-upload.service.ts
import { Injectable } from '@angular/core';
import { HttpClient,HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';  // Import AuthService to get the token

@Injectable({
  providedIn: 'root',
})
export class FileUploadService {

  private apiUrl = 'http://127.0.0.1:8000/api/upload';  // The URL where we will send the file to upload

  constructor(private http: HttpClient, private authService: AuthService,) {}

  uploadFiles(files: File[], uploadType: string = 'drag_and_drop'): Observable<any> {
    const formData = new FormData();
    files.forEach(file => formData.append('file', file, file.name));
    formData.append('upload_type', uploadType); // Add upload-type for use in fileupload_routes.py

    // Get the token from AuthService
    const token = this.authService.getToken();

    // Use append to add Authorization header (important for preserving any existing headers)
    let headers = new HttpHeaders();
    if (token) {
      headers = headers.append('Authorization', `Bearer ${token}`);
    }

    // Make the API request with the token and headers
    return this.http.post(this.apiUrl, formData, { headers });
  }
}