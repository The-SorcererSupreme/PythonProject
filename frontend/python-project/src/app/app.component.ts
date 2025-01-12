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
import { ButtonModule } from 'primeng/button';
import { TreeModule } from 'primeng/tree';

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
    ],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  nodes: TreeNode[] = []; // Tree structure for <p-tree>
  selectedNode: TreeNode | null = null; // Selected node
  loading: boolean = false; // Indicates whether data is being loaded
  currentPath: string = ''; // Keeps track of the current folder path
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
        this.nodes = this.processFolders(data); // Process folder data into tree structure
        this.currentPath = path; // Update current path
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
    processFolders(data: any[]): TreeNode[] {
      return data.map((item) => ({
        label: item.name,
        data: item.isFile ? 'File' : 'Folder',
        icon: item.isFile ? 'pi pi-file' : 'pi pi-folder',
        children: item.children ? this.processFolders(item.children) : undefined,
        leaf: item.isFile
      }));
    }
    
  
    // Event handler for selecting a node
    onNodeSelect(event: any) {
      const node = event.node;
      if (node.data === 'Folder') {
        const folderPath = `${this.currentPath}/${node.label}`;
        this.loadFolderContents(folderPath); // Load contents of selected folder
      } else {
        console.log('Selected file:', node.label);
      }
    }
}
