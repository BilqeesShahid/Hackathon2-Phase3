-- Phase III: AI-Powered Todo Chatbot Tables
-- Add conversations and messages tables without affecting existing Phase II tables

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "userId" TEXT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
  "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updatedAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for conversations
CREATE INDEX IF NOT EXISTS "conversations_userId_idx" ON conversations("userId");
CREATE INDEX IF NOT EXISTS "conversations_userId_updatedAt_idx" ON conversations("userId", "updatedAt");

-- Create message_role enum
DO $$ BEGIN
    CREATE TYPE "MessageRole" AS ENUM ('user', 'assistant');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "conversationId" UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role "MessageRole" NOT NULL,
  content TEXT NOT NULL,
  "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for messages
CREATE INDEX IF NOT EXISTS "messages_conversationId_idx" ON messages("conversationId");
CREATE INDEX IF NOT EXISTS "messages_conversationId_createdAt_idx" ON messages("conversationId", "createdAt");
CREATE INDEX IF NOT EXISTS "messages_createdAt_idx" ON messages("createdAt");
