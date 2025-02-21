import { Component, ChangeDetectorRef } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router, RouterLink } from '@angular/router';
import { NgIf, NgClass } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    NgIf,
    NgClass,
    MatButtonModule,
    MatIconModule,
    ButtonModule,
    RouterLink
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
  constructor(
    public authService: AuthService,
    private router: Router,
    private cdRef: ChangeDetectorRef,
  ) {}

  logout() {
    this.authService.logout();
    this.cdRef.detectChanges();
  }

  isActive(route: string): boolean {
    return this.router.isActive(route, { paths: 'exact', queryParams: 'ignored', fragment: 'ignored', matrixParams: 'ignored' });
  }
}
