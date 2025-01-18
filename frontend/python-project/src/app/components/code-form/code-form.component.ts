import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { FormsModule, FormGroup, FormBuilder, Validators, FormArray } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'code-form-component',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
  ],
  templateUrl: './code-form.component.html',
  styleUrls: ['./code-form.component.css']
})
export class DynamicYamlFormComponent implements OnChanges {
  form: FormGroup; 
  @Input() yamlStructure: any = []; // Receive JSON from the parent component
  constructor(private fb: FormBuilder) {
    this.form= this.fb.group({});
  }


  ngOnChanges(changes: SimpleChanges) {
    if (changes['yamlStructure'] && changes['yamlStructure'].currentValue) {
      // Rebuild the form whenever `yamlStructure` changes
      this.form = this.createFormFromYamlStructure(this.yamlStructure);
      console.log('Received yamlStructure:', this.yamlStructure);
    }
  }

  createFormFromYamlStructure(yamlStructure: any): FormGroup {
    const formGroup = this.fb.group({});
    yamlStructure.forEach((field: any) => {
      if (field.type === 'str') {
        formGroup.addControl(field.name, this.fb.control(field.value || '', Validators.required));
      } else if (field.type === 'int') {
        formGroup.addControl(field.name, this.fb.control(field.value || 0, Validators.min(0)));
      } else if (field.type === 'list') {
        const formArray = this.fb.array(
          field.value.map((v: any) => this.fb.control(v))
        );
        formGroup.addControl(field.name, formArray);
      } else if (field.type === 'dict') {
        formGroup.addControl(field.name, this.createFormFromYamlStructure(field.fields));
      }
    });
    return formGroup;
  }

  // Add a new field to a list in the form
  addFieldToList(name: string) {
    const list = this.yamlStructure.find((item: any) => item.name === name);
    if (list && list.fields) {
      list.fields.push({ type: 'str', value: '' }); // Default to a string field
    }
  }

  // Delete a field from a list
  deleteFieldFromList(name: string, index: number) {
    const list = this.yamlStructure.find((item: any) => item.name === name);
    if (list && list.fields) {
      list.fields.splice(index, 1);
    }
  }

  onSubmit() {
    console.log('Form submitted:', this.form.value);
    // Convert form data back to YAML, if necessary, and send it to backend
  }
}