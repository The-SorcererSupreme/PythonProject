import { TestBed } from '@angular/core/testing';

import { GetContainersService } from './get-containers.service';

describe('GetContainersService', () => {
  let service: GetContainersService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GetContainersService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
