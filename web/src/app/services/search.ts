import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface SearchRequest {
  query: string;
  limit?: number;
}

export interface NoteResult {
  id: string;
  title: string;
  content: string;
  source: string;
  section: string;
  topic: string;
}

export interface SearchResponse {
  hits: NoteResult[];
  query: string;
  estimatedTotalHits: number;
}

export interface AnswerRequest {
  query: string;
  limit?: number;
}

export interface AnswerSource {
  source: string;
  section: string;
  title: string;
}

export interface AnswerResponse {
  answer: string;
  sources: AnswerSource[];
}

@Injectable({
  providedIn: 'root'
})
export class SearchService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;
  // by adding the environment variable above, we can switch between production and development API URLs without changing the code.
  // private apiUrl = 'http://localhost:8000';
  //apiUrl = 'api';

  search(request: SearchRequest): Observable<SearchResponse> {
    return this.http.post<SearchResponse>(`${this.apiUrl}/search`, request);
  }

  answer(request: AnswerRequest): Observable<AnswerResponse> {
    return this.http.post<AnswerResponse>(`${this.apiUrl}/answer`, request);
  }
}