import { Component, ChangeDetectorRef, OnChanges, SimpleChanges, Input } from '@angular/core';
import { FolderService } from '../folder.service';
import { NgIf } from '@angular/common';

@Component({
  selector: 'app-file-content',
  standalone: true,
  imports: [NgIf],
  templateUrl: './file-content.component.html',
  styleUrl: './file-content.component.css'
})
export class FileContentComponent {
  @Input() filePath: string | null = null; // Accept filePath as input
  loading: boolean = false;
  fileContent: string | null = null;
  errorMessage: string | null = null;

  constructor(private folderService: FolderService, private cdr: ChangeDetectorRef) {}
  
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filePath'] && this.filePath) {
      // Call fetchFileContent when the filePath input changes
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

  
}
