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
  constructor(private chatbot: ChatbotService) { }

  getAnswer(question: string) {
    this.questions.push(question);
    this.chatbot.getAnswer(question).subscribe(
      res => {
        let answerStr = '';
        for (const answer of res.results) {
          answerStr += answer + '\n';
        }
        this.answers.push(answerStr);
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
