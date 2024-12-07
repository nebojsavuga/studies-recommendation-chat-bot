import { Injectable } from '@angular/core';
import { environment } from '../../environment/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Answer } from '../models/answer';

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  baseUrl: string = environment.apiHost;

  constructor(private http: HttpClient) { }

  getAnswer(question: string): Observable<Answer> {
    return this.http.post<Answer>(this.baseUrl, { 'user_input': question });
  }
}
