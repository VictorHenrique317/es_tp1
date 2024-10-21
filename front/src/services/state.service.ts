import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { BehaviorSubject } from 'rxjs';

export enum TaskType{
  TRANSCRIPTION = "transcrever",
  SUMMARY = "resumir",
}

export enum TaskProgress{
  IN_PROGRESS,
  DONE,
}

@Injectable({
  providedIn: 'root'
})
export class StateService {
  private file: File | undefined;

  private _current_task = new BehaviorSubject<TaskType | undefined>(undefined);
  private _task_progress = new BehaviorSubject<TaskProgress | undefined>(undefined);
  private _output = new BehaviorSubject<string | undefined>(undefined);

  public current_task$ = this._current_task.asObservable();
  public task_progress$ = this._task_progress.asObservable();
  public output$ = this._output.asObservable();

  constructor(private api_service: ApiService) { }

  public async postVideo(file: File): Promise<void> {
    await this.api_service.postVideo(file);
    this.file = file;
    return;
  }

  public async postAudio(file: File): Promise<void> {
    await this.api_service.postAudio(file);
    this.file = file;
    return;
  }

  public async fetchTranscription(): Promise<void> {
    if (this._task_progress.value == TaskProgress.IN_PROGRESS) {return;}

    this._task_progress.next(TaskProgress.IN_PROGRESS);
    this._current_task.next(TaskType.TRANSCRIPTION);
    this.api_service.getTranscription().then((transcription) => {
      this._output.next(transcription);
      this._task_progress.next(TaskProgress.DONE);

    }).catch((error) => {
      this._current_task.next(undefined);
      this._task_progress.next(undefined);
      this._output.next(undefined);
      throw error;
    });
  }

  public async fetchSummary(): Promise<void> {
    if (this._task_progress.value == TaskProgress.IN_PROGRESS) {return;}

    this._task_progress.next(TaskProgress.IN_PROGRESS);
    this._current_task.next(TaskType.SUMMARY);
    this.api_service.getSummary().then((summary) => {
      this._output.next(summary);
      this._task_progress.next(TaskProgress.DONE);

    }).catch((error) => {
      this._current_task.next(undefined);
      this._task_progress.next(undefined);
      this._output.next(undefined);
      throw error;
    });
  }
}
