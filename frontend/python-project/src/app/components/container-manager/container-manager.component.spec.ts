import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContainerManagerComponent } from './container-manager.component';

describe('ContainerManagerComponent', () => {
  let component: ContainerManagerComponent;
  let fixture: ComponentFixture<ContainerManagerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContainerManagerComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContainerManagerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
