import { Component } from '@angular/core';
import { ChatbotService } from '../../services/chatbot.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent {

  questions: string[] = [];
  answers: string[] = [];
  userInput: string = '';
  loading: boolean = false;

  constructor(private chatbot: ChatbotService) { }

  getAnswer(question: string) {
    this.questions.push(question);
    this.loading = true;

    this.chatbot.getAnswer(question).subscribe(
      res => {
        let answerStr = res.response;
        this.answers.push(answerStr);
        this.loading = false;
      }
    );
  }

  onSubmit(): void {
    if (this.userInput.trim()) {
      this.getAnswer(this.userInput);
      this.userInput = '';
    }
  }
}
