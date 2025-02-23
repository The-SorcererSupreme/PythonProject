import { Component } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { NgIf } from '@angular/common';
import { FileEnvironmentComponent } from '../file-environment/file-environment.component';
import { FileContentComponent } from '../file-content/file-content.component';
import { AngularSplitModule } from 'angular-split';
import { AuthService } from '../../services/auth.service';

@Component({
    selector: 'app-home', // Make sure the component is standalone
    imports: [
        MatToolbarModule,
        NgIf,
        FileEnvironmentComponent,
        FileContentComponent,
        AngularSplitModule,
    ], // Import any modules it depends on
    templateUrl: 'home.component.html',
    styleUrls: ['./home.component.css']
})
export class HomeComponent {
    constructor(public authService: AuthService) {}

    selectedFilePath: string | null = null; // Store the selected file path
    selectedContainerId: string | null = null;

  onFileSelected(data: { filePath: string, containerId: string }) {
    console.log('File path received in AppComponent:', data.filePath);
    console.log('ContainerID received in AppComponent:', data.containerId);
    this.selectedFilePath = data.filePath; // Update the selected file path
    this.selectedContainerId = data.containerId; // Set the container ID
  }
}