import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule, FormControl } from '@angular/forms';

@Component({
  selector: 'code-form-component',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    FormControl,
  ],
  templateUrl: './code-form.component.html',
  styleUrls: ['./code-form.component.css']
})
export class DynamicYamlFormComponent implements OnChanges {
  form: FormGroup;
  @Input() yamlStructure: any = [];

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({});
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['yamlStructure'] && changes['yamlStructure'].currentValue) {
      // Sort yamlStructure by `line_num` to maintain order
      this.yamlStructure.sort((a: any, b: any) => (a.line_num || 0) - (b.line_num || 0));

      // Rebuild the form whenever `yamlStructure` changes
      this.form = this.createFormFromYamlStructure(this.yamlStructure);
      console.log('Updated form with yamlStructure:', this.yamlStructure);
    }
  }

  createFormFromYamlStructure(yamlStructure: any[]): FormGroup {
    const formGroup = this.fb.group({});

    yamlStructure.forEach((field: any) => {
      if (field.type === 'str') {
        formGroup.addControl(field.name, this.fb.control(field.value || '', Validators.required));
      } else if (field.type === 'int') {
        formGroup.addControl(field.name, this.fb.control(field.value || 0, Validators.min(0)));
      } else if (field.type === 'list') {
        const formArray = this.fb.array(
          (field.fields || field.value || []).map((item: any) =>
            typeof item === 'object' ? this.createFormFromYamlStructure(item.fields || []) : this.fb.control(item)
          )
        );
        formGroup.addControl(field.name, formArray);
      } else if (field.type === 'dict') {
        formGroup.addControl(field.name, this.createFormFromYamlStructure(field.fields || []));
      }
    });

    return formGroup;
  }

  addFieldToList(name: string) {
    const list = this.yamlStructure.find((item: any) => item.name === name);
    if (list) {
      const newField = { type: 'str', value: '', line_num: null };
      list.fields = list.fields || [];
      list.fields.push(newField);

      // Get the FormArray and add a new FormControl
      const formArray = this.form.get(name) as FormArray;
      formArray.push(this.fb.control(''));
    }
  }

  deleteFieldFromList(name: string, index: number) {
    const list = this.yamlStructure.find((item: any) => item.name === name);
    if (list && list.fields) {
      list.fields.splice(index, 1);
      (this.form.get(name) as FormArray).removeAt(index);
    }
  }

  getFormArray(name: string): FormArray {
    return this.form.get(name) as FormArray;
  }

  onSubmit() {
    console.log('Form submitted:', this.form.value);
  }
}
