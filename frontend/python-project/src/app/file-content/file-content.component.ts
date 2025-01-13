import { Component, ChangeDetectorRef, OnChanges, SimpleChanges, Input,CUSTOM_ELEMENTS_SCHEMA  } from '@angular/core';
import { FolderService } from '../folder.service';
import { NgIf } from '@angular/common';
import { CodeModel } from '@ngstack/code-editor';

@Component({
  selector: 'app-file-content',
  standalone: true,
  imports: [
    NgIf,
  ],
  templateUrl: './file-content.component.html',
  styleUrl: './file-content.component.css'
})

export class FileContentComponent {
  @Input() filePath: string | null = null; // Accept filePath as input
  loading: boolean = false;
  fileContent: string | null = null;
  fileLanguage: string = 'plaintext'; // Default language
  errorMessage: string | null = null;
  


  theme = 'vs-dark'; // Monaco editor theme
  model: CodeModel = {
    language: 'typescript', // Default language
    uri: 'main.ts',
    value: '// Write your code here...',
  };
  options = {
    contextmenu: true,
    minimap: {
      enabled: true,
    },
  };

  constructor(private folderService: FolderService, private cdr: ChangeDetectorRef) {}
  
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filePath'] && this.filePath) {
      // Call fetchFileContent when the filePath input changes
      this.fileContent = "",
      this.fetchFileContent(this.filePath);
    }
  }

  fetchFileContent(path: string): void { 
    this.loading = true;
    this.errorMessage = null; // Reset error message before fetching
      this.folderService.fetchFileContent(path).subscribe({
        next: (response: any) => {
          if (response.success) {
            this.fileContent = response.content;
            this.fileLanguage = this.getFileLanguage(path); // Detect language
            console.log('Successfuly fetched file content:', this.fileContent);
            this.cdr.markForCheck(); // Trigger Change Detection
          } else {
            console.error('Failed to fetch file content:', response.error);
          }
          this.loading = false;
        },
        error: (err) => {
          console.error('Error fetching file content:', err);
          this.loading = false;
        },
      });
  }

   // Detect language based on file extension
   getFileLanguage(filePath: string): string {
    const extension = filePath.split('.').pop();
    switch (extension) {
      case 'ts': return 'typescript';
      case 'js': return 'javascript';
      case 'html': return 'html';
      case 'css': return 'css';
      case 'json': return 'json';
      case 'java': return 'java';
      case 'py': return 'python';
      default: return 'plaintext';
    }
  }

    // Handle user code changes
    onCodeChange(updatedCode: string): void {
      console.log('Code updated:', updatedCode);
      this.fileContent = updatedCode; // Update file content with edits
  }
}