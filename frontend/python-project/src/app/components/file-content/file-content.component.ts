import { Component, ChangeDetectorRef, OnChanges, SimpleChanges, Input, Output, EventEmitter } from '@angular/core';
import { FolderService } from '../../services/folder.service';
import { NgIf } from '@angular/common';
import { NgxDropzoneModule } from 'ngx-dropzone';

@Component({
  selector: 'app-file-content',
  standalone: true,
  imports: [
    NgIf,
    NgxDropzoneModule,
  ],
  templateUrl: './file-content.component.html',
  styleUrls: ['./file-content.component.css'],
})
export class FileContentComponent {
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
    this.folderService.fetchFileContent(path).subscribe({
      next: (response: any) => {
        if (response.content) {
          this.fileContent = response.content;
          console.log('Successfully fetched file content:', this.fileContent);
          this.cdr.markForCheck(); // Trigger Change Detection
        } else {
          console.error('Failed to fetch file content (API error):', response.error);
          this.errorMessage = 'Failed to fetch file content: ' + response.error;
        }
        this.loading = false;
      },
      error: (err) => {
        console.error('Error fetching file content (HTTP error):', err);
        this.errorMessage = 'Failed to fetch file content: ' + (err.message || 'Unknown error');
        this.loading = false;
      },
    });
  }
}
