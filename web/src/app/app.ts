import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MarkdownComponent } from 'ngx-markdown';

import {
  AnswerResponse,
  NoteResult,
  SearchService
} from './services/search';

@Component({
  selector: 'app-root',
  imports: [FormsModule,
    MarkdownComponent
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  query = '';
  results: NoteResult[] = [];
  totalResults = 0;
  loading = false;
  errorMessage = '';

  answerText = '';
  answerSources: AnswerResponse['sources'] = [];
  answerLoading = false;

  constructor(private searchService: SearchService) {}

  copyText(text: string): void {
    navigator.clipboard.writeText(text);
  }

  search(): void {
    const trimmedQuery = this.query.trim();

    if (!trimmedQuery) {
      this.results = [];
      this.totalResults = 0;
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    this.searchService.search({
      query: trimmedQuery,
      limit: 10
    }).subscribe({
      next: response => {
        this.results = response.hits;
        this.totalResults = response.estimatedTotalHits;
        this.loading = false;
      },
      error: error => {
        console.error(error);
        this.errorMessage = 'Unable to search the Kubernetes notes.';
        this.loading = false;
      }
    });
  }

  async askQuestion(): Promise<void> {
    const trimmedQuery = this.query.trim();

    if (!trimmedQuery) {
      this.answerText = '';
      this.answerSources = [];
      return;
    }

    this.answerText = '';
    this.answerSources = [];
    this.answerLoading = true;
    this.errorMessage = '';

    try {
      const response = await fetch(
        'http://localhost:8000/answer/stream',
        //'/api/answer/stream',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            query: trimmedQuery,
            limit: 5
          })
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      if (!response.body) {
        throw new Error('Streaming response body is unavailable');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });

        const events = buffer.split('\n\n');
        buffer = events.pop() ?? '';

        for (const event of events) {
          if (!event.startsWith('data: ')) {
            continue;
          }

          const jsonText = event.substring('data: '.length);
          const message = JSON.parse(jsonText);

          if (message.type === 'content') {
            this.answerText += message.text;
          }

          if (message.type === 'sources') {
            this.answerSources = message.items;
          }

          if (message.type === 'error') {
            throw new Error(message.message);
          }

          if (message.type === 'done') {
            this.answerLoading = false;
          }
        }
      }

      this.answerLoading = false;
    } catch (error) {
      console.error(error);
      this.errorMessage = 'Unable to stream the answer.';
      this.answerLoading = false;
    }
  }
}