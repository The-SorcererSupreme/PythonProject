import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray, FormControl, AbstractControl } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';
import { DragDropModule } from '@angular/cdk/drag-drop';

@Component({
  selector: 'code-form-component',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    DragDropModule,
  ],
  templateUrl: './code-form.component.html',
  styleUrls: ['./code-form.component.css']
})
export class DynamicYamlFormComponent implements OnChanges {
  form: FormGroup;
  showInsertIndex: number | null = null;
  editingIndex: number | null = null;
  @Input() yamlStructure: any = [];

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({});
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['yamlStructure']?.currentValue) {
      this.yamlStructure.sort((a: any, b: any) => (a.line_num || 0) - (b.line_num || 0));
      this.form = this.createFormFromYamlStructure(this.yamlStructure);
    }
  }

  createFormFromYamlStructure(yamlStructure: any[]): FormGroup {
    const formGroup = this.fb.group({});
    yamlStructure.forEach((field: any) => {
      if (['str', 'int'].includes(field.type)) {
        formGroup.addControl(field.name, new FormControl(field.value || ''));
      } else if (field.type === 'list') {
        formGroup.addControl(field.name, this.fb.array((field.fields || []).map(this.createListItemForm)));
      } else if (field.type === 'dict') {
        formGroup.addControl(field.name, this.createFormFromYamlStructure(field.fields || []));
      }
    });
    return formGroup;
  }

  createListItemForm(subItem: any): FormGroup {
    return subItem.type === 'dict' ? this.createFormFromYamlStructure(subItem.fields || []) : this.fb.group({
      value: new FormControl(subItem.value || ''),
    });
  }

  getFormArray(name: string): FormArray {
    return this.form.get(name) as FormArray;
  }

  addFieldToList(controlName: string): void {
    this.getFormArray(controlName).push(this.fb.group({ value: new FormControl('') }));
  }

  deleteFieldFromList(name: string, index: number): void {
    this.getFormArray(name).removeAt(index);
  }

  editLine(index: number): void {
    this.editingIndex = index;
  }

  saveEdit(): void {
    this.editingIndex = null;
  }

  drop(event: CdkDragDrop<any[]>): void {
    moveItemInArray(this.yamlStructure, event.previousIndex, event.currentIndex);
  }

  moveLine(fromIndex: number, toIndex: number): void {
    if (toIndex >= 0 && toIndex < this.yamlStructure.length) {
      const item = this.yamlStructure.splice(fromIndex, 1)[0];
      this.yamlStructure.splice(toIndex, 0, item);
    }
  }

  insertLine(index: number): void {
    this.yamlStructure.splice(index, 0, { name: '', type: 'str', value: '', show_name: true });
  }

  deleteLine(index: number): void {
    this.yamlStructure.splice(index, 1);
  }
}
