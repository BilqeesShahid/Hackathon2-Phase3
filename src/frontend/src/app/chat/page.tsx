/**
 * AI Chat Page
 *
 * Main page for conversational task management interface.
 * Phase III: AI-Powered Todo Chatbot
 */

"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../../lib/auth-context";
import ChatInterface from "../../components/ChatInterface";
import { ConversationHistorySidebar } from "../../components/ConversationHistorySidebar";

export default function ChatPage() {
  const { user, session, isLoading, signOut } = useAuth();
  const router = useRouter();
  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
  const [conversationKey, setConversationKey] = useState(0);

  useEffect(() => {
    if (!isLoading && !session) {
      router.push("/sign-in");
    }
  }, [session, isLoading, router]);

  const handleSelectConversation = useCallback((conversationId: string) => {
    setSelectedConversationId(conversationId);
    setConversationKey(prev => prev + 1); // Force remount to load conversation
  }, []);

  const handleNewConversation = useCallback(() => {
    setSelectedConversationId(null);
    setConversationKey(prev => prev + 1); // Force remount for new conversation
  }, []);

  const handleSignOut = async () => {
    await signOut();
    router.push("/sign-in");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-violet-500 via-purple-500 to-pink-500">
        <div className="text-white text-xl">Loading...</div>
      </div>
    );
  }

  if (!session || !user) {
    return null;
  }

  return (
    <div className="h-screen flex flex-col overflow-hidden bg-gradient-to-br from-violet-600 via-purple-600 to-pink-600">
      {/* Header */}
      <header className="flex-shrink-0 bg-gradient-to-r from-purple-300/95 via-pink-300/95 to-purple-300/95 backdrop-blur-sm shadow-lg border-b border-purple-400/70 z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-900 to-purple-900 bg-clip-text text-transparent">AI Task Assistant</h1>
              <p className="text-xs text-purple-800">Manage your tasks with natural language</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-purple-950">{user.email}</p>
            </div>
            <button
              onClick={() => router.push("/")}
              className="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg hover:from-blue-600 hover:to-purple-600 transition-all shadow-md hover:shadow-lg items-center gap-2 font-medium"
            >
              <svg className="w-4 h-4 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              Tasks
            </button>
            <button
              onClick={handleSignOut}
              className="px-4 py-2 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-lg hover:from-red-600 hover:to-pink-600 transition-all shadow-md hover:shadow-lg flex items-center gap-2 font-medium"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Chat Interface Container - Fixed height, independent scrolling */}
      <main className="flex-1 flex overflow-hidden relative z-10">
        {/* Sidebar Container - Independent scroll */}
        <div className="flex-shrink-0 w-80 bg-white shadow-xl overflow-hidden">
          <ConversationHistorySidebar
            currentConversationId={selectedConversationId}
            onSelectConversation={handleSelectConversation}
            onNewConversation={handleNewConversation}
          />
        </div>

        {/* Chat Window Container - Independent scroll */}
        <div className="flex-1 bg-white overflow-hidden">
          <ChatInterface
            key={conversationKey}
            selectedConversationId={selectedConversationId}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="flex-shrink-0 bg-gradient-to-r from-purple-300/95 via-pink-300/95 to-purple-300/95 backdrop-blur-sm border-t border-purple-400/70 shadow-lg z-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-center">
            <p className="text-sm text-purple-900">
              <span className="font-semibold">Phase III:</span> AI-Powered Conversational Interface
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
