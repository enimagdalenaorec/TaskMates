import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { StreamTextareaModule, ChannelService } from 'stream-chat-angular';

@Component({
  selector: 'app-custom-message-input',
  standalone: true,
  imports: [CommonModule, FormsModule, StreamTextareaModule],
  template: `
    <div class="custom-message-input">
      <!-- Using the built-in stream-textarea component -->
      <stream-textarea
        [(value)]="textareaValue"
        [placeholder]="placeholder"
        [autoFocus]="autoFocus"
      ></stream-textarea>

      <!-- Custom Send Button -->
      <button
      icon="pi pi-send"
        class="send-button pi pi-send"
        (click)="messageSent()"
        [disabled]="!textareaValue.trim()"
      >
      </button>
    </div>
  `,
  styleUrls: ['./custom-message-input.component.css']
})
export class CustomMessageInputComponent {
  textareaValue = ''; // Binds to textarea input value
  autoFocus = true;
  placeholder = 'Type a message'; // Example placeholder text

  constructor(private channelService: ChannelService) {}

  // This method handles sending the message when the custom send button is triggered
  async messageSent() {
    if (!this.textareaValue.trim()) {
      return; // Prevent sending empty messages
    }

    const channel = this.channelService.activeChannel;
    if (channel) {
      try {
        // Send the message using the active channel
        await channel.sendMessage({ text: this.textareaValue });
        this.textareaValue = ''; // Clear the textarea after sending the message
      } catch (error) {
        console.error('Failed to send message:', error);
      }
    } else {
      console.error('No active channel found.');
    }
  }
}
