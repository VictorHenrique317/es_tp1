import { Injectable } from '@angular/core';

const  API_URL : string = 'http://localhost:80';
const RETRY_DELAY: number = 1000; // 1s
const MAX_RETRIES: number = 300; // 5m

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor() { }

  public async postVideo(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/video`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) { throw new Error(`Failed to upload video: ${response.statusText}`); }
    return response.json();
  }

  public async postAudio (file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/audio`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) { throw new Error(`Failed to upload audio: ${response.statusText}`); }
    return response.json();
  }

  public async getTranscription(query_id: string): Promise<string> {
    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
        const response = await fetch(`${API_URL}/transcription?query_id=${JSON.stringify(query_id)}`, {
            method: 'GET'
        });

        if (response.status === 503) { // Service Unavailable, transcription is not ready, try until it is
            await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
        } else if (response.ok) {
            const data = await response.json();
            const transcriptionLink = `${API_URL}${data.link}`;

            // Fetch the transcription file content
            const transcriptionResponse = await fetch(transcriptionLink, {
                method: 'GET'
            });

            if (transcriptionResponse.ok) {
                return transcriptionResponse.text();
            } else {
                throw new Error(`Error downloading transcription: ${transcriptionResponse.statusText}`);
            }
        } else {
            throw new Error(`Error fetching transcription link: ${response.statusText}`);
        }
    }

    throw new Error('Transcription unavailable after multiple retries.');
  }

  public async getSummary(query_id: string): Promise<string> {
    for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
        const response = await fetch(`${API_URL}/summary?query_id=${JSON.stringify(query_id)}`, {
            method: 'GET'
        });

        if (response.status === 503) { // Service Unavailable, summary is not ready, try until it is
            await new Promise(resolve => setTimeout(resolve, RETRY_DELAY));
        } else if (response.ok) {
            const data = await response.json();
            const summaryLink = `${API_URL}${data.link}`;

            // Fetch the summary file content
            const summaryResponse = await fetch(summaryLink, {
                method: 'GET'
            });

            if (summaryResponse.ok) {
                return summaryResponse.text();
            } else {
                throw new Error(`Error downloading summary: ${summaryResponse.statusText}`);
            }
        } else {
            throw new Error(`Error fetching summary link: ${response.statusText}`);
        }
    }

    throw new Error('Summary unavailable after multiple retries.');
  }
}
