import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideHttpClient } from '@angular/common/http';

// Import your standalone components
import { AppComponent } from './app/app.component';
import { HomeComponent } from './app/home/home.component';
import { Feature1Component } from './app/feature1/feature1.component';
import { Feature2Component } from './app/feature2/feature2.component';

// Define your routes with the standalone components
const routes = [
  { path: '', component: HomeComponent },
  { path: 'feature1', component: Feature1Component },
  { path: 'feature2', component: Feature2Component },
];

// Bootstrap the standalone AppComponent
bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),  // Register routes
    provideAnimations(),     // Provide animations for Angular Material
    provideHttpClient(),
  ],
}).catch((err) => console.error(err));
