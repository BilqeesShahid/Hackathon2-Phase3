"use client";

import { TaskResponse } from "@/lib/api";
import { TaskItem } from "./TaskItem";

interface TaskListProps {
  tasks: TaskResponse[];
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

export function TaskList({ tasks, onTaskUpdated, onTaskDeleted }: TaskListProps) {
  const completedCount = tasks.filter(t => t.completed).length;
  const pendingCount = tasks.length - completedCount;

  if (tasks.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
          <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-gray-800 mb-2">No tasks yet</h3>
        <p className="text-gray-500">Add your first task above to get started!</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex gap-4 mb-4">
        <div className="bg-purple-100 px-4 py-2 rounded-lg">
          <span className="text-purple-700 font-medium">{pendingCount}</span>
          <span className="text-purple-600 text-sm ml-1">pending</span>
        </div>
        <div className="bg-green-100 px-4 py-2 rounded-lg">
          <span className="text-green-700 font-medium">{completedCount}</span>
          <span className="text-green-600 text-sm ml-1">completed</span>
        </div>
      </div>
      <div className="space-y-2">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onTaskUpdated={onTaskUpdated}
            onTaskDeleted={onTaskDeleted}
          />
        ))}
      </div>
    </div>
  );
}
