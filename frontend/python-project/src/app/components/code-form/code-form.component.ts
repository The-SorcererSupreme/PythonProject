import { Component, Input, Output, OnChanges, SimpleChanges, EventEmitter } from '@angular/core';
import { FormGroup, FormBuilder, Validators, FormArray, FormControl, AbstractControl } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { ChangeDetectorRef } from '@angular/core';

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
  showInsertIndex: number | null = null; // Controls visibility of "Add Line" button
  isEditing: number | null = null; // Tracks editing for top-level items
  isEditingMap: { [key: string]: number | null } = {}; // Tracks nested lists/dictionaries
  @Input() yamlStructure: any = [];
  @Output() editingModeChange = new EventEmitter<string>();

  constructor(private fb: FormBuilder, private cdr: ChangeDetectorRef) {
    this.form = this.fb.group({});
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['yamlStructure'] && changes['yamlStructure'].currentValue) {
      this.yamlStructure.sort((a: any, b: any) => (a.line_num || 0) - (b.line_num || 0));
      this.form = this.createFormFromYamlStructure(this.yamlStructure);
      this.editingModeChange.emit('yaml');
      console.log('Updated form with yamlStructure:', this.yamlStructure);
      console.log('To:', this.form);
    }
  }

  // Function to process the YAML structure and create the form
  createFormFromYamlStructure(yamlStructure: any[]): FormGroup {
    const formGroup = this.fb.group({});
  
    yamlStructure.forEach((field: any) => {
      console.log(`Processing item: ${field.name} (type: ${field.type}, show_name: ${field.show_name})`);
  
      if (field.type === 'str' || field.type === 'int') {
        formGroup.addControl(field.name, new FormControl(field.value || '', Validators.required));
        formGroup.addControl(`show_name`, new FormControl(field.show_name !== false));
      } else if (field.type === 'list') {
        const formArray = this.fb.array(
          (field.fields || []).map((subItem: any) => {
            console.log(`  Processing subitem in list: ${subItem.name} (type: ${subItem.type}, show_name: ${subItem.show_name})`);
  
            if (subItem.type === 'dict') {
              const subFormGroup = this.fb.group({});
              subItem.fields.forEach((subField: any) => {
                console.log(
                  `    Processing subfield in dict: ${subField.name} (type: ${subField.type}, show_name: ${subField.show_name})`
                );
  
                subFormGroup.addControl(
                  subField.name,
                  new FormControl(subField.value || '', Validators.required)
                );
                subFormGroup.addControl(`show_name`, new FormControl(subField.show_name !== false));
              });
  
              return subFormGroup;
            } else {
              // Process simple list values (like tags)
              return this.fb.group({
                value: new FormControl(subItem.value || '', Validators.required),
                show_name: new FormControl(subItem.show_name !== false),
              });
            }
          })
        );
        formGroup.addControl(field.name, formArray);
      } else if (field.type === 'dict') {
        console.log(`  Processing nested dictionary: ${field.name}`);
        formGroup.addControl(field.name, this.createFormFromYamlStructure(field.fields || []));
      }
    });
  
    return formGroup;
  }
  getObjectKeys(controls: { [key: string]: AbstractControl<any, any> }): string[] {
    return Object.keys(controls).filter(key => key !== 'show_name');
  }

  getFormGroupControls(control: AbstractControl<any, any>): { [key: string]: AbstractControl<any, any> } {
    return (control as FormGroup).controls;
  }
  
  

  addFieldToList(controlName: string): void {
    const control = this.form.get(controlName) as FormArray;

    const newField = this.fb.group({
      name: new FormControl(''),
      value: new FormControl(''),
      show_name: new FormControl(true),
      type: new FormControl('str'),
      fields: new FormArray([]),
    });

    control.push(newField);
  }

  deleteFieldFromList(name: string, index: number) {
    const list = this.yamlStructure.find((item: any) => item.name === name);
    if (list && list.fields) {
      list.fields.splice(index, 1);
      this.getFormArray(name).removeAt(index);
    }
  }

  getFormArray(name: string): FormArray {
    return this.form.get(name) as FormArray;
  }








    // Show "+ Add Line" Button When Hovered
    showInsertButton(index: number) {
      this.showInsertIndex = index;
    }
  
    hideInsertButton() {
      this.showInsertIndex = null;
    }
  
    // Drag and Drop Function
    drop(event: CdkDragDrop<any[]>) {
      moveItemInArray(this.yamlStructure, event.previousIndex, event.currentIndex);
    }
  
    // Move a Line Up or Down
    moveLine(fromIndex: number, toIndex: number) {
      if (toIndex >= 0 && toIndex < this.yamlStructure.length) {
        const item = this.yamlStructure.splice(fromIndex, 1)[0];
        this.yamlStructure.splice(toIndex, 0, item);
      }
    }

    // Handle Edit button click
    editLine(index: number, listName?: string, subIndex?: number): void {
      if (listName !== undefined && subIndex !== undefined) {
        // Editing inside a list/dictionary
        this.isEditingMap[listName] = subIndex;
      } else {
        // Editing top-level items
        this.isEditing = this.isEditing === index ? null : index;
      }
    
      const item = this.yamlStructure[index];
    
      // Ensure form controls exist before editing
      if (!this.form.controls[`value_${index}`]) {
        this.form.addControl(`value_${index}`, new FormControl(item.value || '', Validators.required));
      }
      
      if (!this.form.controls[`key_${index}`] && item.name) {
        this.form.addControl(`key_${index}`, new FormControl(item.name, Validators.required));
      }
    
      if (!this.form.controls[`comment_${index}`] && item.type === 'comment') {
        this.form.addControl(`comment_${index}`, new FormControl(item.value ?? ''));
      }
      
      if (!this.form.controls[`empty_${index}`] && item.type === 'empty') {
        this.form.addControl(`empty_${index}`, new FormControl(item.value ?? ''));
      }
    
      // Handling Lists and Dictionaries
      if (item.type === 'list') {
        item.fields.forEach((subItem: any, subIndex: number) => {
          const controlKey = `list_${index}_${subIndex}`;
          if (!this.form.controls[controlKey]) {
            this.form.addControl(controlKey, new FormControl(subItem.value || '', Validators.required));
          }
        });
      }
    }

    
    
    saveEdit(index: number, listName?: string): void {
      if (listName !== undefined) {
        this.isEditingMap[listName] = null; // Reset only the nested list/dictionary
        return;
      }
    
      const item = this.yamlStructure[index];
    
      // Store previous type before updating
      const previousType = item.type;
    
      // Update item values
      if (this.form.controls[`value_${index}`]) {
        this.yamlStructure[index].value = this.form.controls[`value_${index}`].value;
      }
    
      if (this.form.controls[`key_${index}`]) {
        this.yamlStructure[index].name = this.form.controls[`key_${index}`].value;
      }
    
      if (this.form.controls[`comment_${index}`]) {
        this.yamlStructure[index].value = this.form.controls[`comment_${index}`].value;
        this.yamlStructure[index].type = 'comment';
      }
    
      if (this.form.controls[`empty_${index}`]) {
        this.yamlStructure[index].value = this.form.controls[`empty_${index}`].value;
        this.yamlStructure[index].type = 'empty';
      }
    
      if (item.type === 'list') {
        item.fields.forEach((subItem: any, subIndex: number) => {
          const controlKey = `list_${index}_${subIndex}`;
          subItem.value = this.form.controls[controlKey].value;
        });
      }
    
      // If the type changed, replace the item in yamlStructure to force re-render
      if (previousType !== this.yamlStructure[index].type) {
        this.yamlStructure[index] = { ...this.yamlStructure[index] };
      }
    
      this.isEditing = null; // Exit edit mode
    
      // Force Angular to detect changes and re-render
      this.cdr.detectChanges();
    
      console.log("Updated YAML Structure:", this.yamlStructure);
    }

  // Handle Submit (Save changes to the form)
  onSubmit(): void {
    // Logic for saving the edited data
    this.isEditing = null;  // Exit edit mode after saving
  }
  
    // Insert a New Line at Specific Index
    insertLine(index: number) {
      this.yamlStructure.splice(index, 0, {
        name: '',
        type: 'str',
        value: '',
        show_name: true
      });
    }
  
    // Delete a Line
    deleteLine(index: number) {
      this.yamlStructure.splice(index, 1);
    }

    trackByIndex(index: number, item: any): number {
      return index;
    }
}