import { Component, OnInit } from '@angular/core';
import { ContainerService } from '../../services/get-containers.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-container-manager',
  standalone: true,
  imports: [
    NgIf,
    NgFor,
    FormsModule,
  ],
  templateUrl: './container-manager.component.html',
  styleUrl: './container-manager.component.css'
})
export class ContainerManagerComponent implements OnInit {
  containers: any[] = [];
  editingContainerId: string | null = null;
  loadingContainerId: string | null = null;
  selectedContainerId: string | null = null;
  usersWithAccess: any[] = [];
  newUsername: string = "";
  errorMessage: string | null = null;

  constructor(private containerService: ContainerService, private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchContainers();
  }

  fetchContainers(): void {
    this.containerService.getContainers(false).subscribe(  // Fetch only owned containers
      (response) => {
        this.containers = response.containers;
        this.errorMessage = null;
      },
      (error) => {
        this.errorMessage = 'Error fetching containers.';
        console.error(error);
      }
    );
  }

  startContainer(containerId: string) {
    this.containerService.startContainer(containerId).subscribe(
      () => {
        console.log(`Container ${containerId} started.`);
        this.fetchContainers();
      },
      (error) => console.error('Error starting container:', error)
    );
  }

  stopContainer(containerId: string) {
    this.loadingContainerId = containerId;
    this.containerService.stopContainer(containerId).subscribe(
      () => {
        console.log(`Container ${containerId} stopped.`);
        this.loadingContainerId = null;
        this.fetchContainers();
      },
      (error) => {
        console.error('Error stopping container:', error);
        this.loadingContainerId = null;
      }
    );
  }

  deleteContainer(container: any, isRunning: boolean) {
    if (isRunning) {
      alert("You must stop the container before deleting it.");
      return;
    }

    if (!confirm(`Are you sure you want to delete container ${container.container_name}?`)) return;
    if (!confirm(`This action is irreversible. Do you really want to delete container ${container.container_name}?`)) return;

    this.containerService.deleteContainer(container.id).subscribe(
      () => {
        console.log(`Container ${container.container_name} deleted.`);
        this.fetchContainers();
      },
      (error) => console.error('Error deleting container:', error)
    );
  }

  editContainerName(containerId: string) {
    console.log("Editing container: " + containerId)
    this.editingContainerId = containerId;
  }

  saveContainerName(container: any, newName: string) {
    if (!newName.trim() || newName === container.container_name) {
      this.editingContainerId = null; // Exit edit mode if no change
      return;
    }
  
    this.containerService.updateContainerName(container.id, newName).subscribe(
      () => {
        console.log(`Container name updated to: ${newName}`);
        container.container_name = newName; // Update UI immediately
        this.editingContainerId = null; // Exit edit mode
      },
      (error) => {
        console.error('Error updating container name:', error);
        alert('Failed to update container name. Please try again.');
      }
    );
  }

  onContainerNameBlur(event: Event, container: any) {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement) {
      this.saveContainerName(container, inputElement.value);
    }
  }


    // Toggle the Manage Access section for a specific container
    toggleManageAccess(containerId: string) {
      if (this.selectedContainerId === containerId) {
        this.selectedContainerId = null; // Close the form if it's already open
      } else {
        this.selectedContainerId = containerId;
        this.getContainerAccess(containerId); // Load shared users
      }
    }
  
    // Fetch users who have access to the container
    getContainerAccess(containerId: string) {
      this.containerService.getContainerAccess(containerId).subscribe(
        (response) => {
          this.usersWithAccess = response.users_with_access;
        },
        (error) => {
          console.error("Error fetching access info:", error);
        }
      );
    }
  
    // Share container with a new user by username
    shareAccess(containerId: string) {
      if (!this.newUsername.trim()) return; // Prevent empty submissions
  
      this.containerService.shareContainer(containerId, this.newUsername).subscribe(
        (response) => {
          console.log(response.message);
          this.getContainerAccess(containerId); // Refresh shared users list
          this.newUsername = ""; // Clear input field
        },
        (error) => {
          console.error("Error sharing container access:", error);
        }
      );
    }
  
    // Revoke access for a specific user
    revokeAccess(containerId: string, userId: string) {
      this.containerService.revokeAccess(containerId, userId).subscribe(
        (response) => {
          console.log(response.message);
          this.getContainerAccess(containerId); // Refresh shared users list
        },
        (error) => {
          console.error("Error revoking container access:", error);
        }
      );
    }
}
