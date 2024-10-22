import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import { StateService, TaskType } from 'src/services/state.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit, OnDestroy{
  @ViewChild('fileInput', { static: false }) fileInput!: ElementRef;
  
  protected file: File | undefined;
  protected task_output_text: string = 'Saída';
  protected task_in_progress: boolean = false;
  protected output: string | undefined;

  private subscriptions: Subscription[] = [];

  constructor(private state_service: StateService) {}

  ngOnInit(): void {
    let file_subscription = this.state_service.file$.subscribe((file) => {
      this.file = file;
    });
    this.subscriptions.push(file_subscription);

    let current_task_subscription = this.state_service.current_task$.subscribe((task) => {
      if (task === TaskType.TRANSCRIPTION){
        this.task_output_text = 'Saída - Transcrição';
      }
      else if (task === TaskType.SUMMARY){
        this.task_output_text = 'Saída - Resumo';
      }
      else{
        this.task_output_text = 'Saída';
      }
    });
    this.subscriptions.push(current_task_subscription);

    let task_in_progress_subscription = this.state_service.task_in_progress$.subscribe((task_in_progress) => {
      this.task_in_progress = task_in_progress;
    });
    this.subscriptions.push(task_in_progress_subscription);

    let output_subscription = this.state_service.output$.subscribe((output) => {
      this.output = output;
    });
    this.subscriptions.push(output_subscription);
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(subscription => subscription.unsubscribe());
  }

  protected selectFile(){
    this.fileInput.nativeElement.click();
  }

  protected onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file: File = input.files[0]; // Get the first selected file
      this.state_service.setFile(file);
    }
  }

  protected upload(){
    this.state_service.postFile();
  }

  protected async fetchTranscription(): Promise<void> {
    this.state_service.fetchTranscription();
  }

  protected async fetchSummary(): Promise<void> {
    this.state_service.fetchSummary();
  }
}
