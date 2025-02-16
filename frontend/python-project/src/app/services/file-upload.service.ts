import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';  // Import AuthService to get the token

@Injectable({
  providedIn: 'root',
})
export class FileUploadService {
  private apiUrl = 'http://127.0.0.1:8000/api/upload';  // The backend API endpoint

  constructor(private http: HttpClient, private authService: AuthService) {}

  uploadFiles(formData: FormData, uploadType: string = 'drag_and_drop'): Observable<any> {

    /* // Append each file and ensure dynamic archive name is included
    files.forEach(file => {
      formData.append('file', file, file.name);
      formData.append('archive_name', file.name); // Ensure archive name is included
    });*/

    formData.append('upload_type', uploadType); // Optional: Specify upload type

    // Get the token from AuthService
    const token = this.authService.getToken();

    // Create headers
    let headers = new HttpHeaders();
    if (token) {
      headers = headers.append('Authorization', `Bearer ${token}`);
    }

    // Make the API request with headers
    return this.http.post(this.apiUrl, formData, { headers });
  }
}
