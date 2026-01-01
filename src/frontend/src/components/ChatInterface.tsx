/**
 * Chat Interface Component
 *
 * Conversational UI for task management using a chat-style interface.
 *
 * Note: OpenAI ChatKit is used conceptually here. In production, you might use:
 * - A custom chat UI component
 * - @chatscope/chat-ui-kit-react
 * - react-chat-elements
 *
 * Constitution Compliance:
 * - JWT token management (§6.1)
 * - Stateless UI (loads from backend)
 */

'use client';

import { useState, useEffect, useRef } from 'react';
import { useChat } from '../hooks/useChat';
import TaskMessageRenderer from './TaskMessageRenderer';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

interface ChatInterfaceProps {
  onConversationChange?: () => void;
  selectedConversationId?: string | null;
}

export default function ChatInterface({ onConversationChange, selectedConversationId }: ChatInterfaceProps = {}) {
  const { messages, sendMessage, isLoading, error, loadConversation, clearConversation } = useChat();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load selected conversation on mount
  useEffect(() => {
    if (selectedConversationId) {
      loadConversation(selectedConversationId);
    } else {
      clearConversation();
    }
  }, [selectedConversationId, loadConversation, clearConversation]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    await sendMessage(userMessage);
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 scrollbar-thin">
        {messages.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center text-gray-400 h-full">
            <div className="w-20 h-20 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-4">
              <svg className="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h3 className="text-2xl font-semibold text-gray-800 mb-2">AI Task Assistant</h3>
            <p className="text-gray-500 text-sm">Ask me to add, list, update, complete, or delete tasks</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`py-6 ${
              msg.role === 'user' ? 'bg-white' : 'bg-gray-50'
            }`}
          >
            <div className="max-w-3xl mx-auto flex gap-4">
              {/* Avatar */}
              <div className={`w-9 h-9 rounded-full flex-shrink-0 flex items-center justify-center ${
                msg.role === 'user' ? 'bg-gradient-to-r from-blue-600 to-purple-600' : 'bg-green-600'
              }`}>
                {msg.role === 'user' ? (
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                )}
              </div>

              {/* Content */}
              <div className="flex-1 text-gray-800">
                {msg.role === 'assistant' ? (
                  <TaskMessageRenderer content={msg.content} />
                ) : (
                  <div className="whitespace-pre-wrap">{msg.content}</div>
                )}
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="py-6 bg-gray-50">
            <div className="max-w-3xl mx-auto flex gap-4">
              <div className="w-9 h-9 rounded-full flex-shrink-0 bg-green-600 flex items-center justify-center">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div className="flex-1 flex items-center">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="p-4">
            <div className="max-w-3xl mx-auto bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
              {error}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="flex-shrink-0 p-4 bg-white border-t border-gray-200">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
          <div className="relative flex items-center bg-gray-100 rounded-2xl border border-gray-300 shadow-sm focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-100 transition-all">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Send a message... (e.g., 'Show my tasks')"
              className="flex-1 bg-transparent text-gray-800 px-5 py-4 pr-14 focus:outline-none placeholder-gray-400"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="absolute right-2 bottom-2 p-2.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-md"
            >
              {isLoading ? (
                <svg className="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
                </svg>
              )}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-3 text-center">
            💡 Try: "Add buy milk" • "Show my tasks" • "Show pending tasks" • "Complete task 1"
          </p>
        </form>
      </div>
    </div>
  );
}
