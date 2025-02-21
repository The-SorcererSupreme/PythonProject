/// <reference types="@angular/localize" />

//frontend/python-project/src/main.ts

// Import your standalone AppComponent
import { AppComponent } from './app/app.component';

// Import other things
import { routes } from './app/app.routes';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideHttpClient } from '@angular/common/http';
import { provideCodeEditor } from '@ngstack/code-editor';

// Bootstrap the standalone AppComponent
bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),  // Register routes
    provideAnimations(),   // Provide animations
    provideHttpClient(),   // HTTP client for API calls
    provideCodeEditor(),   // Code editor functionality
  ],
}).catch((err) => console.error(err));
