// src/app/components/containers/containers.component.ts
import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { ContainerService } from '../../services/get-containers.service';
import { FormsModule } from '@angular/forms';
import { NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-containers',
  standalone: true,
  templateUrl: './containers.component.html',
  styleUrls: ['./containers.component.css'],
  imports: [
    NgIf,
    NgFor,
    FormsModule],
})
export class ContainersComponent implements OnInit {
  @Output() containerSelected = new EventEmitter<string>(); // Emit selected container ID

  containers: any[] = [];
  selectedContainerId: string = '';

  errorMessage: string | null = null;

  constructor(private containerService: ContainerService,) { }

  ngOnInit(): void {
    // Get all available containers
    this.fetchContainers();  
  
    // Retrieve the last selected container from localStorage
    const savedContainerId = localStorage.getItem('selectedContainerId');
    if (savedContainerId) {
      this.selectedContainerId = savedContainerId;
      
      // Emit the value so the parent component updates accordingly
      this.containerSelected.emit(this.selectedContainerId);
    }
  }

  fetchContainers(): void {
    this.containerService.getContainers(true).subscribe(  // Pass true to include shared containers
      (response) => {
        this.containers = response.containers;
        this.errorMessage = null;
  
        // Clear localStorage if no containers are available
        if (this.containers.length === 0) {
          localStorage.removeItem('folderStructure');
          localStorage.removeItem('selectedContainerId');
          console.log('Cleared folderStructure from localStorage because no containers are available.');
        }
      },
      (error) => {
        this.errorMessage = 'Error fetching containers. Please try again later.';
        console.error(error);
      }
    );
  }

  onSelectContainer(event: any) {
    this.selectedContainerId = event.target.value;
    console.log('Selected container:', this.selectedContainerId);
    
    // Store in localStorage
    localStorage.setItem('selectedContainerId', this.selectedContainerId);
  
    // Emit selection
    this.containerSelected.emit(this.selectedContainerId);
  }

  // Method to refresh the container list
  refreshContainers() {
    this.fetchContainers();  // Re-fetch the containers
  }
}
