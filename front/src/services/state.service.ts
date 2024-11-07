import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { BehaviorSubject } from 'rxjs';

export enum TaskType{
  TRANSCRIPTION = "transcrever",
  SUMMARY = "resumir",
}

@Injectable({
  providedIn: 'root'
})
export class StateService {
  private _file = new BehaviorSubject<File | undefined>(undefined);
  private _current_task = new BehaviorSubject<TaskType | undefined>(undefined);
  private _task_in_progress = new BehaviorSubject<boolean>(false);
  private _output = new BehaviorSubject<string | undefined>(undefined);

  public file$ = this._file.asObservable();
  public current_task$ = this._current_task.asObservable();
  public task_in_progress$ = this._task_in_progress.asObservable();
  public output$ = this._output.asObservable();

  private db_id: string | undefined;

  constructor(private api_service: ApiService) { }

  public setFile(file: File): void {
    this._file.next(file);
  }

  private async postVideo(): Promise<void> {
    if (this._file.value){
      let data = await this.api_service.postVideo(this._file.value);
      this.db_id = data.db_id;
    }
    
    return;
  }

  private async postAudio(): Promise<void> {
    if (this._file.value){
      let data = await this.api_service.postAudio(this._file.value);
      this.db_id = data.db_id;
    }

    return;
  }

  public async postFile(): Promise<void> {
    if (!this._file.value){ return ;}

    this._task_in_progress.next(true);
    if (this._file.value.type.startsWith('audio/')) {
      await this.postAudio();
    }else if (this._file.value.type.startsWith('video/')) {
      await this.postVideo();
    }
    this._task_in_progress.next(false);

    return;
  }

  public async fetchTranscription(): Promise<void> {
    if (this._task_in_progress.value) {return;}
    if (!this.db_id) {return;}

    this._task_in_progress.next(true);
    this._current_task.next(TaskType.TRANSCRIPTION);
    this._output.next(undefined);
    this.api_service.getTranscription(this.db_id).then((transcription) => {
      this._output.next(transcription);
      this._task_in_progress.next(false);

    }).catch((error) => {
      this._current_task.next(undefined);
      this._task_in_progress.next(false);
      this._output.next(undefined);
      throw error;
    });
  }

  public async fetchSummary(): Promise<void> {
    if (this._task_in_progress.value) {return;}
    if (!this.db_id) {return;}

    this._task_in_progress.next(true);
    this._current_task.next(TaskType.SUMMARY);
    this._output.next(undefined);
    this.api_service.getSummary(this.db_id).then((summary) => {
      this._output.next(summary);
      this._task_in_progress.next(false);

    }).catch((error) => {
      this._current_task.next(undefined);
      this._task_in_progress.next(false);
      this._output.next(undefined);
      throw error;
    });
  }
}
