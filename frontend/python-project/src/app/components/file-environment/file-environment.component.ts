// /frontend/python-project/src/app/components/file-environment/file-environment.component.ts
import { Component, OnInit, EventEmitter, Output, Inject, PLATFORM_ID, ViewChild } from '@angular/core';
import { FolderService } from '../../services/folder.service';
import { TreeModule } from 'primeng/tree';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FileContentComponent } from '../../components/file-content/file-content.component';
import { FileUploadService } from '../../services/file-upload.service';
import { NgxDropzoneModule } from 'ngx-dropzone'; // Import the dropzone module
import { NgIf, NgFor, isPlatformBrowser } from '@angular/common';
import { ContainersComponent } from '../containers/containers.component';
import { MenuItem } from 'primeng/api';
import { ContextMenu } from 'primeng/contextmenu';

interface TreeNode {
  label: string;
  data?: any;
  children?: TreeNode[];
  leaf?: boolean; // Indicates whether the node is a leaf (no children)
  path?: string;  // Add path property to store the full file/folder path
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
    ContextMenu,
  ],
  providers: [
    FileContentComponent
  ],
  templateUrl: './file-environment.component.html',
  styleUrl: './file-environment.component.css'
})


export class FileEnvironmentComponent /*implements OnInit*/ {
  @ViewChild(ContainersComponent) containersComponent!: ContainersComponent;  // Reference to ContainersComponent
  @ViewChild(ContextMenu) menu!: ContextMenu;
  @Output() fileSelected = new EventEmitter<{ filePath: string, containerId: string }>(); // Emit selected file path
  
  loading: boolean = false; // Indicates whether data is being loaded
  nodes: TreeNode[] = []; // Tree structure for <p-tree>
  selectedNode: TreeNode | null = null; // Selected node
  currentPath: string = ''; // Keeps track of the current folder path
  fileContent: string | null = null; // Content of the selected file
  files: File[] = [];
  contentLoaded = false;
  selectedContainerId: string | null = null; // Store the container ID persistently
  menuItems: MenuItem[] = [];
  
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
     this.menuItems = [
       { label: 'Download', icon: 'pi pi-download', command: () => this.downloadFile() }
      ];
      
      // Retrieve the last selected container ID
      if (isPlatformBrowser(this.platformId)) {
        const savedContainerId = localStorage.getItem('selectedContainerId');
        if (savedContainerId) {
          this.selectedContainerId = savedContainerId;
          this.loadContainerFolderStructure(savedContainerId);
          console.log("Container ID in storage: " + savedContainerId)
        }
      }
    }
    
    onContainerSelected(containerId: string) {
      console.log('Received selected container:', containerId);
      if (containerId) {
        this.selectedContainerId = containerId;
        localStorage.setItem('selectedContainerId', containerId); // Store in localStorage
        this.loadContainerFolderStructure(containerId);
      }
    }  
    
    // Event handler for selecting a node
    onNodeSelect(event: any) {
      console.log("Left-click event:", event);
      const node = event.node;
      console.log("Node selected: " + node.data)
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
    
    onRightClick(event: any) {
      event.preventDefault();  // Prevent the default context menu
      
      // If node is not provided in the event, fallback to the selectedNode
      const node = event.node || this.selectedNode;
    
      if (node) {
        console.log("Right-click detected on node:", node);
        console.log("Node data:", node.data);  // This should be 'File' or 'Folder'
        
        // Check the type of the node (file or folder) and update the menu accordingly
        if (node.data === 'File') {
          this.menuItems = [
            { label: 'Download File', icon: 'pi pi-download', command: () => this.downloadFile() }
          ];
        } else if (node.data === 'Folder') {
          this.menuItems = [
            { label: 'Download Folder', icon: 'pi pi-download', command: () => this.downloadFile() }
          ];
        }
    
        // Show the custom context menu
        if (this.menu) {
          this.menu.show(event);
        }
      } else {
        console.error("No valid node found in right-click event.");
      }
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
        localStorage.removeItem('selectedContainerId');
        if (this.containersComponent) {
          this.containersComponent.refreshContainers(); // Refresh the container component
        }
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
          localStorage.setItem('selectedContainerId', response.containerId);

          this.loading = false;
          this.contentLoaded = true;
          console.log('Folder structure received from backend:', this.nodes);
          // After successful upload, refresh the container list
          if (this.containersComponent) {
            this.containersComponent.refreshContainers(); // Refresh the container component
          }
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
  

  // Function to trigger file download
  downloadFile() {
    if (!this.selectedNode || !this.selectedNode.path) {
      console.error("No file selected for download.");
      return;
    }
  
    const filePath = this.selectedNode.path;
    const fileName = this.selectedNode.label; // Use label for file name
    const token = localStorage.getItem("auth_token");
    
    if (!token) {
      console.error("No authentication token found!");
      return;
    }
  
    const headers = new HttpHeaders({ Authorization: `Bearer ${token}` });
  
    this.http.get(`http://localhost:8000/api/download?filePath=${filePath}`, {
      headers,
      responseType: 'blob' // Handle binary data (file download)
    }).subscribe({
      next: (blob) => {
        const a = document.createElement('a');
        const url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName; // Name of the file being downloaded
        document.body.appendChild(a);
        a.click();
  
        // Prevent the download link from retaining focus after the click
        setTimeout(() => {
          window.URL.revokeObjectURL(url);
          document.body.removeChild(a);
        }, 0);
      },
      error: (error) => console.error("Download failed:", error)
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