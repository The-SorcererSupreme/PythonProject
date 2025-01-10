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

interface FolderNode {
  name: string;
  children?: FolderNode[];
  isFile?: boolean;  // Add an optional isFile property to distinguish files from folders
}

interface FlatNode {
  expandable: boolean;
  name: string;
  level: number;
  isFile: boolean;  // Add isFile property here as well
}

@Component({
  selector: 'app-root',
  standalone: true,  // Ensure this flag is present
  imports: [
    RouterOutlet,      // Importing necessary modules for standalone
    RouterLink,
    RouterLinkActive,
    CommonModule,
    MatSidenavModule,
    MatToolbarModule,
    MatListModule,
    MatIconModule,
    MatButtonModule,
    MatTreeModule,
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
  folders: any[] = []; // Add this declaration
  currentPath: string = ''; // Add this declaration


  constructor(private folderService: FolderService) {}

  toggleSidenav(sidenav: any) {
    sidenav.toggle();
  }

  ngOnInit() {
    this.loadFolderContents();
  }

  loadFolderContents(path: string = '') {
    this.folderService.getFolderContents(path).subscribe((data: any) => {
      this.folders = data.folders || [];
      this.currentPath = data.currentPath || '';
    });
  }

  navigateToFolder(folderName: string) {
    this.loadFolderContents(`${this.currentPath}/${folderName}`);
  }

  navigateToParentFolder() {
    const parentPath = this.currentPath.substring(0, this.currentPath.lastIndexOf('/')) || '';
    this.loadFolderContents(parentPath);
  }

  private transformer = (node: FolderNode, level: number) => {
    return {
      expandable: !!node.children && node.children.length > 0,
      name: node.name,
      level,
      isFile: node.isFile || false,
    };
  };

  treeControl = new FlatTreeControl<FlatNode>(
    (node) => node.level,
    (node) => node.expandable
  );

  treeFlattener = new MatTreeFlattener(
    this.transformer,
    (node) => node.level,
    (node) => node.expandable,
    (node) => node.children
  );

  dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);

  hasChild = (_: number, node: FlatNode) => node.expandable;
}
