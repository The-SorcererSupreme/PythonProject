import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MaterialModule } from './material.module';
import { RouterModule, Routes } from '@angular/router';
import { HttpClient } from '@angular/common/http'; // Use this for module-based apps
//import { provideCodeEditor } from '@ngstack/code-editor';
//import { EditorModule } from 'primeng/editor';

// Import components that aren't standalone (if needed, otherwise omit them)
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { Feature1Component } from './feature1/feature1.component';
import { Feature2Component } from './feature2/feature2.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'feature1', component: Feature1Component },
  { path: 'feature2', component: Feature2Component },
];

@NgModule({
  declarations: [
    AppComponent, // Register your AppComponent
    HomeComponent,
    Feature1Component,
    Feature2Component,
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes), // Register the routes here
    MaterialModule, // Register your Material Module
    HttpClient,
    //EditorModule,
  ],
  providers: [
    //provideCodeEditor(),
  ],
  bootstrap: [AppComponent], // Set the bootstrap component
})
export class AppModule {}