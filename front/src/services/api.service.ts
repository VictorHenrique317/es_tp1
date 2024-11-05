import { Injectable } from '@angular/core';

const  API_URL : string = 'http://localhost:80';
const RETRY_DELAY: number = 1000; // 1s
const MAX_RETRIES: number = 300; // 5m

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor() { }

  public async postVideo(file: File): Promise<void> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/video`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) { throw new Error(`Failed to upload video: ${response.statusText}`); }
    return;
  }

  public async postAudio (file: File): Promise<void> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/audio`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) { throw new Error(`Failed to upload audio: ${response.statusText}`); }
    return;
  }

  public async getTranscription(): Promise<string> {
    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
      const response = await fetch(`${API_URL}/transcription`);
  
      if (response.status === 503) { // Service Unavailable, transcription is not ready, try until it is
        await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
      } else if (response.ok) {
        return response.json();
      } else {
        throw new Error(`Error fetching transcription: ${response.statusText}`);
      }
    }
    
    throw new Error('Transcription unavailable after multiple retries.');
  }

  public async getSummary(): Promise<string> {
    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
      const response = await fetch(`${API_URL}/summary`);
  
      if (response.status === 503) { // Service Unavailable, summary is not ready, try until it is
        await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
      } else if (response.ok) {
        return response.json();
      } else {
        throw new Error(`Error fetching summary: ${response.statusText}`);
      }
    }
    
    throw new Error('Summary unavailable after multiple retries.');
  }
}
