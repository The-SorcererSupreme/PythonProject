// /frontend/python-project/src/app/auth.guard.ts
import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(
    private router: Router,
    private authService: AuthService,
    @Inject(PLATFORM_ID) private platformId: Object // Inject platform ID
  ) {}

  canActivate(): boolean {
    if (this.authService.isLoggedIn()) {
      return true;
    }
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('auth_token'); // Ensure 'auth_token' matches what you store in AuthService
      if (!token) {
        this.router.navigate(['/login']); // Redirect to login if no token
        return false;
      }
    }
    return true;
  }
}
