import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FileEnvironmentComponent } from './file-environment.component';

describe('FileEnvironmentComponent', () => {
  let component: FileEnvironmentComponent;
  let fixture: ComponentFixture<FileEnvironmentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FileEnvironmentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FileEnvironmentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
