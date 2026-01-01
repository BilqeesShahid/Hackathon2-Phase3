/**
 * Task Message Renderer Component
 *
 * Custom renderer for task lists in chat messages.
 * Detects and formats task list messages with nice styling.
 *
 * Constitution Compliance:
 * - Stateless UI component (§6.1)
 */

'use client';

import React from 'react';

interface Task {
  id: number;
  title: string;
  completed: boolean;
}

interface TaskMessageRendererProps {
  content: string;
}

/**
 * Parse task list from backend response
 *
 * Expected formats:
 * - "Here are your tasks (N total):"
 * - "**Pending:**"
 * - "  1. Task title"
 * - "**Completed:**"
 * - "  ~~2. Task title~~"
 */
function parseTaskList(content: string): Task[] | null {
  // Check if this is a task list message
  if (!content.includes('**Pending:**') && !content.includes('**Completed:**') && !content.includes('Here are your')) {
    return null;
  }

  const tasks: Task[] = [];
  const lines = content.split('\n');

  for (const line of lines) {
    // Match patterns like "  1. Task title" or "  ~~2. Task title~~"
    const match = line.match(/^\s*(~~)?(\d+)\.\s*(.+?)(~~)?$/);
    if (match) {
      const isCompleted = !!match[1]; // Has strikethrough
      const id = parseInt(match[2]);
      const title = match[3].trim();

      tasks.push({
        id,
        title,
        completed: isCompleted,
      });
    }
  }

  return tasks.length > 0 ? tasks : null;
}

export default function TaskMessageRenderer({ content }: TaskMessageRendererProps) {
  const tasks = parseTaskList(content);

  // If not a task list, render as plain text
  if (!tasks) {
    return <div className="whitespace-pre-wrap">{content}</div>;
  }

  // Extract header (first line before tasks)
  const lines = content.split('\n');
  const header = lines[0] || 'Your tasks:';

  // Group tasks by completion status
  const pendingTasks = tasks.filter(t => !t.completed);
  const completedTasks = tasks.filter(t => t.completed);

  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="font-medium text-gray-700">{header}</div>

      {/* Pending Tasks */}
      {pendingTasks.length > 0 && (
        <div>
          <div className="text-sm font-semibold text-gray-600 mb-2">Pending</div>
          <div className="space-y-1">
            {pendingTasks.map((task) => (
              <div
                key={task.id}
                className="flex items-start gap-2 p-2 bg-blue-50 rounded-md hover:bg-blue-100 transition-colors"
              >
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500 text-white text-xs flex items-center justify-center font-medium">
                  {task.id}
                </div>
                <div className="flex-1 text-sm text-gray-800 pt-0.5">
                  {task.title}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Completed Tasks */}
      {completedTasks.length > 0 && (
        <div>
          <div className="text-sm font-semibold text-gray-600 mb-2">Completed</div>
          <div className="space-y-1">
            {completedTasks.map((task) => (
              <div
                key={task.id}
                className="flex items-start gap-2 p-2 bg-gray-50 rounded-md opacity-75"
              >
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500 text-white text-xs flex items-center justify-center font-medium">
                  ✓
                </div>
                <div className="flex-1 text-sm text-gray-500 line-through pt-0.5">
                  {task.title}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty state */}
      {tasks.length === 0 && (
        <div className="text-sm text-gray-500 italic">
          No tasks found. Add one to get started!
        </div>
      )}
    </div>
  );
}
