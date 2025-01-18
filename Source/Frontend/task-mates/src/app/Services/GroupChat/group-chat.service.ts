// chat.service.ts
import { Injectable } from '@angular/core';
import { Client as TwilioClient } from '@twilio/conversations';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private client: TwilioClient | null = null;

  constructor(private http: HttpClient) {}

  // Fetch token from Django backend
  async initialize(identity: string) {
    const response = await this.http
      .get<{ token: string }>('http://localhost:8000/twilio/token/?identity=${identity}')
      .toPromise();
    const token = response?.token;

    this.client = await TwilioClient.create(token!);
    console.log('Twilio client initialized');
  }

  // Create or join a conversation
  async getOrCreateConversation(conversationSid: string) {
    if (!this.client) {
      throw new Error('Twilio client is not initialized');
    }

    let conversation;
    try {
      conversation = await this.client.getConversationBySid(conversationSid);
    } catch {
      conversation = await this.client.createConversation({ uniqueName: conversationSid });
    }

    return conversation;
  }

  // Send a message
  async sendMessage(conversation: any, message: string) {
    if (!conversation) throw new Error('Conversation is not available');
    await conversation.sendMessage(message);
  }

  // Subscribe to new messages
  onNewMessage(conversation: any, callback: Function) {
    conversation.on('messageAdded', (message: any) => callback(message));
  }
}