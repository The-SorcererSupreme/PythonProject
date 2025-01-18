import { Component, ChangeDetectorRef, OnChanges, SimpleChanges, Input, Output, EventEmitter } from '@angular/core';
import { FolderService } from '../../services/folder.service';
import { NgIf } from '@angular/common';
import { NgxDropzoneModule } from 'ngx-dropzone';
import { DynamicYamlFormComponent } from '../code-form/code-form.component';

@Component({
  selector: 'app-file-content',
  standalone: true,
  imports: [
    NgIf,
    NgxDropzoneModule,
    DynamicYamlFormComponent,
  ],
  templateUrl: './file-content.component.html',
  styleUrls: ['./file-content.component.css'],
})
export class FileContentComponent {
  yamlData: any = []; // Data passed to the child component
  @Input() filePath: string | null = null; // Accept filePath as input
  @Output() fileContentChange = new EventEmitter<any>(); // Output to emit the file content
  loading: boolean = false;
  fileContent: any = null; // Store the JSON content here
  errorMessage: string | null = null;

  constructor(private folderService: FolderService, private cdr: ChangeDetectorRef) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filePath'] && this.filePath) {
      this.fileContent = null; // Reset the content
      this.fetchFileContent(this.filePath);
    }
  }

  fetchFileContent(path: string): void {
    this.loading = true;
    this.errorMessage = null; // Reset error message before fetching

    // Clear previous data
    this.fileContent = null;
    this.yamlData = null;
  
    this.folderService.fetchFileContent(path).subscribe({
      next: (response: any) => {
        // Check if the response has a "data" field (for YAML files)
        if (response.success) {
          if (response.data) {
            // Handle YAML structure (JSON array)
            this.yamlData = response.data;
            console.log('YAML Data:', this.yamlData);
          } else if (typeof response.content === 'string') {
            // Handle plain file content
            this.fileContent = response.content;
            console.log('File Content:', this.fileContent);
          }
        } else {
          console.error('API error:', response.error);
          this.errorMessage = 'Failed to fetch file content: ' + response.error;
        }
        this.loading = false;
        this.cdr.markForCheck(); // Trigger Change Detection
      },
      error: (err) => {
        console.error('Error fetching file content (HTTP error):', err);
        this.errorMessage = 'Failed to fetch file content: ' + (err.message || 'Unknown error');
        this.loading = false;
      },
    });
  }
  
}
