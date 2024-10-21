import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { StateService, TaskType } from 'src/services/state.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit{
  @ViewChild('fileInput', { static: false }) fileInput!: ElementRef;
  
  protected current_task: TaskType | undefined;

  constructor(private state_service: StateService) {}

  ngOnInit(): void {
    this.state_service.current_task$.subscribe((task) => {
      this.current_task = task;
    });
  }

  protected  upload(){
    this.fileInput.nativeElement.click();
  }

  protected onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file: File = input.files[0]; // Get the first selected file
      if (file.type.startsWith('audio/')) {
        this.state_service.postAudio(file);
      }else if (file.type.startsWith('video/')) {
        this.state_service.postVideo(file);
      }
    }
  }
}
