/**
 * Chat API Client
 *
 * Handles communication with the backend chat endpoint.
 *
 * Constitution Compliance:
 * - JWT token attached to all requests (§7.2)
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  message: string;
  conversation_id?: string | null;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
}

export class ChatApiClient {
  private async getAuthToken(): Promise<string> {
    // Get JWT token from Better Auth session
    // This should integrate with your existing auth system
    const token = localStorage.getItem('auth_token');
    if (!token) {
      throw new Error('No authentication token found');
    }
    return token;
  }

  async sendMessage(
    userId: string,
    message: string,
    conversationId?: string | null
  ): Promise<ChatResponse> {
    const token = await this.getAuthToken();

    const response = await fetch(`${API_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Chat request failed: ${response.statusText}`
      );
    }

    return response.json();
  }
}

// Singleton instance
export const chatApi = new ChatApiClient();
