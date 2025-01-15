import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray } from '@angular/forms';

@Component({
  selector: 'app-dynamic-yaml-form',
  imports: [],
  templateUrl: './dynamic-yaml-form.component.html',
  styleUrls: ['./dynamic-yaml-form.component.css']
})
export class DynamicYamlFormComponent {
  form: FormGroup;
  yamlStructure: any; // This will hold the structure from the backend

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({});
  }

  // This method will be triggered after the YAML file is parsed by the backend
  createFormFromYamlStructure(yamlStructure: any) {
    // Recursively build the form from the YAML structure
    const formGroup = this.fb.group({});
    yamlStructure.forEach((field: any) => {
      if (field.type === 'string') {
        formGroup.addControl(field.name, this.fb.control(field.value || '', Validators.required));
      } else if (field.type === 'boolean') {
        formGroup.addControl(field.name, this.fb.control(field.value || false));
      } else if (field.type === 'integer') {
        formGroup.addControl(field.name, this.fb.control(field.value || 0, Validators.min(0)));
      } else if (field.type === 'list') {
        // For lists, we add an array of form controls (dynamic fields)
        formGroup.addControl(field.name, this.fb.array(field.value ? field.value.map((v: any) => this.fb.control(v)) : []));
      } else if (field.type === 'object') {
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
