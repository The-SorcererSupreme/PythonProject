import { Component, ChangeDetectorRef, OnChanges, SimpleChanges, Input, Output, EventEmitter, ElementRef, AfterViewInit, ViewChild, inject } from '@angular/core';
import { FolderService } from '../../services/folder.service';
import { CommonModule, NgIf, NgFor } from '@angular/common';
import { NgxDropzoneModule } from 'ngx-dropzone';
import { DynamicYamlFormComponent } from '../code-form/code-form.component';
import { FormsModule } from '@angular/forms';
import { Subject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';


@Component({
  selector: 'app-file-content',
  standalone: true,
  imports: [
    NgIf,
    NgxDropzoneModule,
    DynamicYamlFormComponent,
    CommonModule,
    NgFor,
    FormsModule,
    MatSnackBarModule,
  ],
  templateUrl: './file-content.component.html',
  styleUrls: ['./file-content.component.css'],
})
export class FileContentComponent implements OnChanges, AfterViewInit {
  private inputSubject: Subject<void> = new Subject<void>(); // Define the debounce subject
  yamlData: any = []; // Data passed to the child component
  @Input() filePath: string | null = null; // File path to fetch content
  @Input() selectedContainerId: string | null = ''; // Container ID to send the request to
  @Output() fileContentChange = new EventEmitter<any>(); // Output to emit the file content

  loading: boolean = false;
  fileContent: any = null;
  errorMessage: string | null = null;
  pathParts: string[] = [];

  @ViewChild('editor', { static: false }) editor!: ElementRef;
  @ViewChild('lineNumbers', { static: false }) lineNumbers!: ElementRef;

  private snackBar = inject(MatSnackBar);

  constructor(private folderService: FolderService, private cdr: ChangeDetectorRef) {
    this.inputSubject.pipe(debounceTime(1000)).subscribe(() => {
      this.updateLineNumbers(); // Update line numbers after debounce period
    });
  }


   // Runs after view is fully initialized
  ngAfterViewInit(): void {
    this.cdr.detectChanges();
    this.updateLineNumbers();
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log('Change detected:', changes);
    console.log('Current filePath:', this.filePath);
    console.log('Current containerId:', this.selectedContainerId);
  
    // Ensure values persist even if they arrive at different times
    const filePathChanged = changes['filePath'] && this.filePath;
    const containerChanged = changes['containerSelected'] && this.selectedContainerId;

    if (this.filePath) {
      this.pathParts = this.filePath.split('/').filter(part => part !== '');
    }

    if (this.filePath && this.selectedContainerId) {
      console.log('Both filePath and containerId are set. Fetching content...');
      this.fileContent = null; // Reset the content
      this.fetchFileContent(this.filePath, this.selectedContainerId);
    } else {
      console.log('Waiting for both values to be set.');
    }

    if (changes['fileContent'] && this.fileContent !== null) {
      console.log("New file content:", this.fileContent);
      this.updateLineNumbers();
    }
  }

  fetchFileContent(path: string, containerId: string): void {
    this.loading = true;
    this.errorMessage = null;

    // Clear previous data
    this.fileContent = null;
    this.yamlData = null;

    this.folderService.fetchFileContent(path, containerId).subscribe({
      next: (response: any) => {
        if (response.success) {
          if (response.data) {
            this.yamlData = response.data;
            console.log('YAML Data:', this.yamlData);
          } else if (typeof response.content === 'string') {
            this.fileContent = response.content;
            //this.fileContent = "function hello() {\n  console.log('Hello World');\n}"; //static test
            console.log('File Content (fetch file):', this.fileContent);
          }
        } else {
          console.error('API error:', response.error);
          this.errorMessage = 'Failed to fetch file content: ' + response.error;
        }
        this.loading = false;
        this.cdr.markForCheck(); // Trigger Change Detection
        //this.updateLineNumbers();

        // Delay line number update until the next cycle
        setTimeout(() => {
          this.updateLineNumbers();  // Update line numbers after view has been updated
        });
      },
      error: (err) => {
        console.error('Error fetching file content:', err);
        this.errorMessage = 'Failed to fetch file content: ' + (err.message || 'Unknown error');
        this.loading = false;
      },
    });
  }

  updateFileContent(event: Event): void {
    console.log("File content:", this.fileContent); // ✅ Debugging Step 3
    
    const target = event.target as HTMLElement;
    this.fileContent = target.innerText; // Update content
    this.updateLineNumbers();
  }

  onEditorInput(): void {
    // Notify the subject to trigger debounce
    this.inputSubject.next();
  }
  
  updateLineNumbers(): void {
    console.log("Updating line numbers...");

    if (!this.fileContent) {
      this.lineNumbers.nativeElement.innerHTML = "";
      return;
    }

    const lines = this.fileContent.split("\n").length;
    let lineNumbersHtml = "";

    for (let i = 1; i <= lines; i++) {
      lineNumbersHtml += `<div>${i}</div>`;
    }

    this.lineNumbers.nativeElement.innerHTML = lineNumbersHtml;
  }

  syncScroll(): void {
    // Get the scroll position of the textarea
    const textarea = this.editor.nativeElement;
    const lineNumbersElement = this.lineNumbers.nativeElement;
  
    // Sync the scroll position of the line numbers container with the textarea
    lineNumbersElement.scrollTop = textarea.scrollTop;
  }

  navigateTo(index: number) {
    const newPath = '/' + this.pathParts.slice(0, index + 1).join('/');
    console.log('Navigating to:', newPath);
    // Later, implement a function to load the new directory or file content.
  }
  
  saveChanges() {
    if (!this.filePath || !this.selectedContainerId) {
      console.error('File path or container ID is missing.');
      this.errorMessage = 'File path or container ID is missing.';
      return;
    }
  
    // Get the content from the editor
    const updatedContent = this.editor.nativeElement.value;
    console.log("Content to save: " + updatedContent)
  
    // Call the backend API to save the content
    this.folderService.saveFileContent(this.filePath, this.selectedContainerId, updatedContent).subscribe({
      next: (response: any) => {
        const responseData = Array.isArray(response) ? response[0] : response;
        if (responseData.success) {
          console.log('File saved successfully!');
          this.fileContentChange.emit(updatedContent); // Emit the new content to notify parent component
          this.showNotification('File saved successfully!', 'success');
        } else {
          console.error('Save error:', responseData.error);
          this.errorMessage = 'Failed to save file content: ' + responseData.error;
          this.showNotification('Failed to save file', 'error');
        }
      },
      error: (err) => {
        console.error('Error saving file content:', err);
        this.errorMessage = 'Failed to save file content: ' + (err.message || 'Unknown error');
        this.showNotification('Failed to save file content', 'error');
      },
    });
  }

  private showNotification(message: string, type: 'success' | 'error') {
    console.log('Message: ' + message + type);
    this.snackBar.open(message, 'Close', {
      duration: 10000,
      panelClass: type === 'success' ? 'snackbar-success' : 'snackbar-error',
      verticalPosition: 'bottom',
      horizontalPosition: 'right',
    });
  }

  reloadFile() {
    if (this.filePath && this.selectedContainerId) {
      console.log('Reloading file...');
      this.fetchFileContent(this.filePath, this.selectedContainerId);
    }
  }
  
  closeFile() {
    console.log('Closing file...');
    this.fileContent = null;
  }
}
