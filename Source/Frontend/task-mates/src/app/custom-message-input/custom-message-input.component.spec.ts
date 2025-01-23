import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomMessageInputComponent } from './custom-message-input.component';

describe('CustomMessageInputComponent', () => {
  let component: CustomMessageInputComponent;
  let fixture: ComponentFixture<CustomMessageInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CustomMessageInputComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CustomMessageInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
