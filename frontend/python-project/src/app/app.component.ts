// /frontend/python-project/src/app/app.component.ts
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTreeModule } from '@angular/material/tree';
import { CommonModule } from '@angular/common';
import { AngularSplitModule } from 'angular-split';
import { ButtonModule } from 'primeng/button';
import { ReactiveFormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';

//import { CodeEditorComponent, CodeModel } from '@ngstack/code-editor';
import { FileEnvironmentComponent } from './components/file-environment/file-environment.component';
import { FileContentComponent } from './components/file-content/file-content.component';
import { DynamicYamlFormComponent} from './code-form/code-form.component'
@Component({
    selector: 'app-root',
    standalone: true,
    imports: [
        NgIf,
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
        DynamicYamlFormComponent,
        ReactiveFormsModule,
        //CodeEditorComponent,
        FileEnvironmentComponent,
        FileContentComponent
    ],
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent {
  //loading: boolean = false; // Indicates whether data is being loaded
  //nodes: TreeNode[] = []; // Tree structure for <p-tree>
  //selectedNode: TreeNode | null = null; // Selected node
  //currentPath: string = ''; // Keeps track of the current folder path
  //fileContent: string | null = null; // Content of the selected file

  //constructor(private folderService: FolderService, private http: HttpClient) {}

  selectedFilePath: string | null = null; // Store the selected file path

  onFileSelected(filePath: string): void {
    console.log('File path received in AppComponent:', filePath);
    this.selectedFilePath = filePath; // Update the selected file path
  }

  // Toggles the side navigation menu
  toggleSidenav(sidenav: any) {
    sidenav.toggle();
  }
}
