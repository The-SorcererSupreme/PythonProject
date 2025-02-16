// /frontend/python-project/src/app/components/file-environment/file-environment.component.ts
import { Component, OnInit, EventEmitter, Output, Inject, PLATFORM_ID } from '@angular/core';
import { FolderService } from '../../services/folder.service';
import { TreeModule } from 'primeng/tree';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FileContentComponent } from '../../components/file-content/file-content.component';
import { FileUploadService } from '../../services/file-upload.service';
import { NgxDropzoneModule } from 'ngx-dropzone'; // Import the dropzone module
import { NgIf, NgFor, isPlatformBrowser } from '@angular/common';
import { ContainersComponent } from '../containers/containers.component';

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
    NgxDropzoneModule,
    NgIf,
    NgFor,
    ContainersComponent,
  ],
  providers: [
    FileContentComponent
  ],
  templateUrl: './file-environment.component.html',
  styleUrl: './file-environment.component.css'
})


export class FileEnvironmentComponent /*implements OnInit*/ {
  @Output() fileSelected = new EventEmitter<{ filePath: string, containerId: string }>(); // Emit selected file path

  loading: boolean = false; // Indicates whether data is being loaded
  nodes: TreeNode[] = []; // Tree structure for <p-tree>
  selectedNode: TreeNode | null = null; // Selected node
  currentPath: string = ''; // Keeps track of the current folder path
  fileContent: string | null = null; // Content of the selected file
  files: File[] = [];
  contentLoaded = false;
  selectedContainerId: string | null = null; // Store the container ID persistently

  constructor(private folderService: FolderService,
    private loadContent: FileContentComponent,
    private fileUploadService: FileUploadService,
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object // Inject PLATFORM_ID  
  ) {}

  /*ngOnInit() {
    this.loadFolderContents();
  }*/
    ngOnInit() {
      this.loadFolderStructureFromStorage();
    }
  
    loadFolderStructureFromStorage() {
      if (isPlatformBrowser(this.platformId)) {
        const savedStructure = localStorage.getItem('folderStructure');
        if (savedStructure) {
          this.nodes = JSON.parse(savedStructure);
          console.log('Loaded folder structure from localStorage:', this.nodes);
          this.contentLoaded = true;
        } else {
          console.log('No folder structure found in localStorage.');
        }
      }
    }
  
    clearFolderStructure() {
      if (isPlatformBrowser(this.platformId)) {
        localStorage.removeItem('folderStructure');
      }
      this.nodes = [];
      this.contentLoaded = false;
      console.log('Folder structure cleared.');
    }

  // Call this function when a container is selected
  loadContainerFolderStructure(containerId: string) {
    console.log('Fetching folder structure for container:', containerId);
  
    this.loading = true; // Show loading indicator
  
    // Retrieve the token from localStorage or a service
    const token = localStorage.getItem("auth_token"); // Adjust if you store the token elsewhere
  
    if (!token) {
      console.error("No token found! User might not be authenticated.");
      this.loading = false;
      return;
    }
  
    // Set up HTTP headers with the Bearer token
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  
    this.http.get(`http://localhost:8000/api/file-structure?containerId=${containerId}`, { headers }).subscribe({
      next: (data: any) => {
        // Handle the folder structure here
        this.nodes = this.processFolders(data);
        this.contentLoaded = true;
        console.log("Updated folder structure from container:", this.nodes);
        this.loading = false; // Hide loading indicator
      },
      error: (err) => {
        console.error('Error fetching folder structure:', err);
        this.nodes = []; // Reset nodes on error
        this.loading = false; // Hide loading indicator
      }
    });
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
        this.contentLoaded = true;
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

  onContainerSelected(containerId: string) {
    console.log('Received selected container:', containerId);
    if (containerId) {
      this.selectedContainerId = containerId; // Store it for later use
      this.loadContainerFolderStructure(containerId);
    }
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
      if (node.path && this.selectedContainerId) {
        console.log("Fetching file content with container ID:", this.selectedContainerId);
        this.fileSelected.emit({
          filePath: node.path,
          containerId: this.selectedContainerId
        });
      } else {
        console.error('File path missing for selected node');
      }
    }
  }

  onDrop(event: any) {
    console.log('Drop event:', event);
  
    if (event && event.addedFiles && event.addedFiles.length > 0) {
      this.files = event.addedFiles;
      console.log('Files dropped:', this.files);
  
      // Extract the file name dynamically
      const archiveName = this.files[0].name;
      console.log('Extracted archive name:', archiveName);
  
      // Pass the extracted file name to uploadFiles function
      this.uploadFiles(this.files, archiveName);
    } else {
      console.log('No files added.');
    }
  }
  
  uploadFiles(files: File[], archiveName: string) {
    const formData = new FormData();
    formData.append('file', files[0]); // Append the file
    formData.append('archive_name', archiveName); // Send the actual archive name
  
    this.fileUploadService.uploadFiles(formData).subscribe({
      next: (response) => {
        console.log('Upload successful:', response);
        console.log('File Structure:', response.file_structure);
  
        if (response && response.file_structure) {
          this.nodes = this.processFolders(response.file_structure, '');
          localStorage.setItem('folderStructure', JSON.stringify(this.nodes));
  
          this.loading = false;
          this.contentLoaded = true;
          console.log('Folder structure received from backend:', this.nodes);
        }
      },
      error: (error) => {
        console.error('Upload failed:', error);
        this.nodes = [];
        this.loading = false;
      },
      complete: () => {
        console.log('File upload process completed.');
      }
    });
  }
  
  

  // Placeholder methods for button actions
  connectToGit() {
    console.log('Connect to Git clicked');
  }

  connectViaAgent() {
    console.log('Connect via Agent clicked');
  }

}