// src/app/components/containers/containers.component.ts
import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { ContainerService } from '../../services/get-containers.service';
import { NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-containers',
  standalone: true,
  templateUrl: './containers.component.html',
  styleUrls: ['./containers.component.css'],
  imports: [NgIf, NgFor],
})
export class ContainersComponent implements OnInit {
  @Output() containerSelected = new EventEmitter<string>(); // Emit selected container ID

  containers: any[] = [];
  selectedContainerId: string = '';

  errorMessage: string | null = null;

  constructor(private containerService: ContainerService,) { }

  ngOnInit(): void {
    this.fetchContainers();  // Call fetchContainers when the component is loaded
  }

  fetchContainers(): void {
    this.containerService.getContainers().subscribe(
      (response) => {
        this.containers = response.containers;
        this.errorMessage = null;
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
    this.containerSelected.emit(this.selectedContainerId); // Emit selection
  }
}
