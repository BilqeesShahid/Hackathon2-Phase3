/**
 * useChat Hook
 *
 * Manages chat state and handles message sending.
 */

'use client';

import { useState, useCallback } from 'react';
import { useAuth } from '../lib/auth-context';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function useChat() {
  const { user, session } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    if (!user || !session) {
      setError('User not authenticated');
      return;
    }

    // Add user message to UI immediately
    const userMessage: Message = { role: 'user', content };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Get token from session
      const token = (session as any).token || '';

      console.log('[Chat Debug] Sending message:', {
        userId: user.id,
        messageLength: content.length,
        hasToken: !!token,
        apiUrl: API_URL,
        conversationId
      });

      // Send to backend
      const response = await fetch(`${API_URL}/api/${user.id}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: content,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Chat request failed: ${response.statusText}`);
      }

      const data = await response.json();

      // Update conversation ID if new
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add assistant response to UI
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response,
      };
      setMessages(prev => [...prev, assistantMessage]);

    } catch (err: any) {
      console.error('[Chat Debug] Error details:', {
        error: err,
        message: err.message,
        stack: err.stack
      });
      setError(err.message || 'Failed to send message');
      console.error('Chat error:', err);
      // Remove user message on error
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  }, [user, session, conversationId]);

  const clearConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  }, []);

  const loadConversation = useCallback(async (convId: string) => {
    if (!user || !session) {
      setError('User not authenticated');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const token = (session as any).token || '';

      // Fetch conversation messages from backend
      const response = await fetch(`${API_URL}/api/${user.id}/conversations/${convId}/messages`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to load conversation');
      }

      const data = await response.json();

      // Set messages and conversation ID
      setMessages(data.messages || []);
      setConversationId(convId);

    } catch (err: any) {
      console.error('Error loading conversation:', err);
      setError(err.message || 'Failed to load conversation');
    } finally {
      setIsLoading(false);
    }
  }, [user, session]);

  return {
    messages,
    sendMessage,
    isLoading,
    error,
    conversationId,
    clearConversation,
    loadConversation,
  };
}
