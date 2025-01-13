import { Component,OnInit,EventEmitter,Output } from '@angular/core';
import { FolderService } from '../folder.service';
import { TreeModule } from 'primeng/tree';
import { FileContentComponent } from '../file-content/file-content.component';

interface TreeNode {
  label: string;
  data?: any;
  children?: TreeNode[];
  leaf?: boolean; // Indicates whether the node is a leaf (no children)
}

@Component({
  selector: 'app-file-environment',
  standalone: true,
  imports: [
    TreeModule,
    FileContentComponent,
  ],
  providers: [
    FileContentComponent
  ],
  templateUrl: './file-environment.component.html',
  styleUrl: './file-environment.component.css'
})


export class FileEnvironmentComponent implements OnInit {
  @Output() fileSelected = new EventEmitter<string>(); // Emit selected file path

  loading: boolean = false; // Indicates whether data is being loaded
  nodes: TreeNode[] = []; // Tree structure for <p-tree>
  selectedNode: TreeNode | null = null; // Selected node
  currentPath: string = ''; // Keeps track of the current folder path
  fileContent: string | null = null; // Content of the selected file

  constructor(private folderService: FolderService, private loadContent: FileContentComponent) {}

  ngOnInit() {
    this.loadFolderContents();
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
        console.log("Entering fetchFile content")
        this.fileSelected.emit(node.path); // Emit the file path to the parent
      } else {
        console.error('File path missing for selected node');
      }
    }
  }
}