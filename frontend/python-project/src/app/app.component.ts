import { Component, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTreeModule } from '@angular/material/tree';
import { CommonModule } from '@angular/common';
import { FolderService } from './folder.service';
import { ChangeDetectorRef } from '@angular/core';
import { AngularSplitModule } from 'angular-split';
import { ButtonModule } from 'primeng/button';
import { TreeModule } from 'primeng/tree';
import { CodeEditorComponent, CodeModel } from '@ngstack/code-editor';
import { HttpClient } from '@angular/common/http';

interface TreeNode {
  label: string;
  data?: any;
  children?: TreeNode[];
  leaf?: boolean; // Indicates whether the node is a leaf (no children)
}

@Component({
    selector: 'app-root',
    imports: [
        RouterOutlet,
        RouterLink,
        RouterLinkActive,
        CommonModule,
        MatSidenavModule,
        MatToolbarModule,
        MatListModule,
        MatIconModule,
        MatButtonModule,
        MatTreeModule,
        AngularSplitModule,
        ButtonModule,
        TreeModule,
        CodeEditorComponent,
    ],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  loading: boolean = false; // Indicates whether data is being loaded
  nodes: TreeNode[] = []; // Tree structure for <p-tree>
  selectedNode: TreeNode | null = null; // Selected node
  currentPath: string = ''; // Keeps track of the current folder path
  fileContent: string | null = null; // Content of the selected file
  isResizing: boolean = false;
  startX: number = 0;
  startWidth: number = 0;

  constructor(private folderService: FolderService, private http: HttpClient) {}

  ngOnInit() {
    this.loadFolderContents();
  }

  // Toggles the side navigation menu
  toggleSidenav(sidenav: any) {
    sidenav.toggle();
  }

  startResize(event: MouseEvent) {
    this.isResizing = true;
    this.startX = event.clientX;
  
    // Cast to HTMLElement for proper type
    const sidenav = document.querySelector('.mat-sidenav') as HTMLElement;
    this.startWidth = sidenav.clientWidth;
  
    document.addEventListener('mousemove', this.resizeSidebar.bind(this));
    document.addEventListener('mouseup', this.stopResize.bind(this));
  }
  
  resizeSidebar(event: MouseEvent) {
    if (this.isResizing) {
      const offset = event.clientX - this.startX;
      
      // Cast to HTMLElement for proper type
      const sidenav = document.querySelector('.mat-sidenav') as HTMLElement;
      const newWidth = this.startWidth + offset;
      sidenav.style.width = `${newWidth}px`;
    }
  }
  
  stopResize() {
    this.isResizing = false;
    document.removeEventListener('mousemove', this.resizeSidebar.bind(this));
    document.removeEventListener('mouseup', this.stopResize.bind(this));
  }

  // Loads the contents of the current folder or a specified path
  loadFolderContents(path: string = '') {
    console.log('Loading contents for path:', path); // Debug log
    this.loading = true; // Show loading indicator
    this.folderService.getFolderContents(path).subscribe({
      next: (data: any) => {
        this.nodes = this.processFolders(data, path); // Pass current path when processing data
        this.currentPath = path; // Update current path
        console.log(path)
        console.log(this.currentPath)
        this.loading = false; // Hide loading indicator
      },
      error: (err) => {
        console.error('Error loading folder contents:', err);
        this.nodes = []; // Reset tree nodes on error
        this.loading = false; // Hide loading indicator
      }
    });
  }
  

    // Processes raw folder data into a tree structure
    processFolders(data: any[], currentPath: string = ''): TreeNode[] {
      //console.log('Processing folder data for path:', currentPath); // Debug log
    
      return data.map((item) => {
        const fullPath = `${currentPath}/${item.name}`; // Generate full path for the node
        const nodePath = item.path || fullPath; // Generate full path for the node
        //console.log('Generated full path for node:', fullPath); // Debug log
    
        return {
          label: item.name,
          data: item.isFile ? 'File' : 'Folder',
          isFile: item.isFile, // Indicates whether it's a file
          path: nodePath, // Add full path to the node
          icon: item.isFile ? 'pi pi-file' : 'pi pi-folder', // Optional: Set icons for file and folder
          leaf: item.isFile, // Mark files as leaf nodes
          children: item.children ? this.processFolders(item.children, fullPath) : [],
        };
      });
    }
    
    
  
    // Event handler for selecting a node
    onNodeSelect(event: any) {
      const node = event.node;
      if (node.data === 'Folder') {
        // Use the full path to load the folder's contents
        const folderPath = node.path;  // Ensure that path exists
        console.log('Navigating to folder:', folderPath); // Debug log
        this.loadFolderContents(folderPath);
      } else if (node.data === 'File') {
        console.log('Selected file:', node.label);
        if (node.path) {
          this.fetchFileContent(node.path);  // Send full file path for the request
        } else {
          console.error('File path missing for selected node');
        }
      }
    }

    // GET FILE CONTENT
  
    // Fetch the content of the selected file
  fetchFileContent(path: string): void {
    this.loading = true;
    this.folderService.fetchFileContent(path).subscribe({
      next: (response: any) => {
        if (response.success) {
          this.fileContent = response.content;
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

    //Code-Editor

}
