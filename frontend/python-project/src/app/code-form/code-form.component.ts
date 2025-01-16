import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'code-form-component',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './code-form.component.html',
  styleUrls: ['./code-form.component.css']
})
export class DynamicYamlFormComponent {
  form: FormGroup;
  @Input() yamlStructure: any = []; // Receive JSON from the child component

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({});
  }

  // This method will be triggered after the YAML file is parsed by the backend
  createFormFromYamlStructure(yamlStructure: any) {
    const formGroup = this.fb.group({});
    yamlStructure.forEach((field: any) => {
      if (field.type === 'str') {  // Adjusted for the correct type
        formGroup.addControl(field.name, this.fb.control(field.value || '', Validators.required));
      } else if (field.type === 'int') {
        formGroup.addControl(field.name, this.fb.control(field.value || 0, Validators.min(0)));
      } else if (field.type === 'list') {
        // Handle list (array)
        const formArray = this.fb.array(
          field.value.map((v: any) => this.fb.control(v))
        );
        formGroup.addControl(field.name, formArray);
      } else if (field.type === 'dict') {
        // Handle nested objects
        formGroup.addControl(field.name, this.createFormFromYamlStructure(field.fields));
      }
    });
    return formGroup;
  }

  // Add a new field to a list in the form
  addFieldToList(name: string) {
    const formArray = (this.form.get(name) as FormArray);
    formArray.push(this.fb.control(''));
  }

  // Delete a field from a list
  deleteFieldFromList(name: string, index: number) {
    const formArray = (this.form.get(name) as FormArray);
    formArray.removeAt(index);
  }

  onSubmit() {
    console.log(this.form.value);
    // Convert form data back to YAML, if necessary, and send it to backend
  }
}
