import { Component, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTreeModule } from '@angular/material/tree';
import { FlatTreeControl } from '@angular/cdk/tree';
import { MatTreeFlatDataSource, MatTreeFlattener } from '@angular/material/tree';
import { CommonModule } from '@angular/common';
import { FolderService } from './folder.service';
import { ChangeDetectorRef } from '@angular/core';
import { AngularSplitModule } from 'angular-split';

interface FolderNode {
  name: string;
  children?: FolderNode[];
  isFile?: boolean;
}

interface FlatNode {
  expandable: boolean;
  name: string;
  level: number;
  isFile: boolean;
  padding?: number;  // Add the padding property to the interface
}

@Component({
  selector: 'app-root',
  standalone: true,
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
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  folders: FolderNode[] = []; // Processed folder data for display
  currentPath: string = ''; // Keeps track of the current folder path
  loading: boolean = false; // Indicates whether data is being loaded
  isResizing: boolean = false;
  startX: number = 0;
  startWidth: number = 0;

  constructor(private folderService: FolderService) {}

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
    this.loading = true; // Show loading indicator
    this.folderService.getFolderContents(path).subscribe({
      next: (data: any) => {
        console.log('API Response:', data); // Debug: Log raw API response
        this.folders = this.processFolders(data); // Process folder structure
        this.currentPath = path; // Update current path
        this.updateTreeData(); // Refresh the tree view
        this.loading = false; // Hide loading indicator
        // Simulate window resize to force a reflow
        window.dispatchEvent(new Event('resize'));
      },
      error: (err) => {
        console.error('Error loading folder contents:', err);
        this.folders = []; // Reset folders on error
        this.updateTreeData(); // Clear the tree view
        this.loading = false; // Hide loading indicator
      },
    });
  }

  // Processes the raw folder data recursively
  processFolders(data: any[]): FolderNode[] {
    return data.map((item) => ({
      name: item.name,
      isFile: item.isFile,
      children: item.children ? this.processFolders(item.children) : [],
    }));
  }

  // Updates the MatTree data source
  updateTreeData() {
    console.log('Updating Tree Data:', this.folders); // Debug: Log processed folders
    console.log('Updating Tree Data (final):', this.folders);
    this.dataSource.data = this.folders;
  }

  // Navigates into a folder
  navigateToFolder(folderName: string) {
    this.loadFolderContents(`${this.currentPath}/${folderName}`);
  }

  // Navigates to the parent folder
  navigateToParentFolder() {
    const parentPath = this.currentPath.substring(0, this.currentPath.lastIndexOf('/')) || '';
    this.loadFolderContents(parentPath);
  }

  // Determines whether a node is expandable (has children)
  private transformer = (node: FolderNode, level: number): FlatNode => {
    return {
      expandable: !!node.children && node.children.length > 0,
      name: node.name,
      level,
      isFile: node.isFile || false,
      padding: level * 16,  // Add padding for each level
    };
  };

  // Checks if a node has children
  hasChild = (_: number, node: FlatNode) => node.expandable;

  // Expands a node to load its contents
  onExpand(node: FlatNode) {
    if (!node.isFile) {
      const fullPath = `${this.currentPath}/${node.name}`;
      this.loadFolderContents(fullPath);
    }
  }

  // Tree control for managing expandable/collapsible nodes
  treeControl = new FlatTreeControl<FlatNode>(
    (node) => node.level,
    (node) => node.expandable
  );

  // Flattens the nested folder structure for MatTree
  treeFlattener = new MatTreeFlattener(
    this.transformer,
    (node) => node.level,
    (node) => node.expandable,
    (node) => node.children
  );

  // Data source for the MatTree component
  dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);
}
