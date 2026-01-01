/*Dashboard page for Phase II Todo Application.*/
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "../lib/auth-context";
import { TaskList } from "../components/TaskList";
import { Sidebar } from "../components/Sidebar";
import { TaskResponse, getTasks } from "@/lib/api";

export default function DashboardPage() {
  const { user, session, isLoading, signOut } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<TaskResponse[]>([]);
  const [tasksLoading, setTasksLoading] = useState(true);
  const [error, setError] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    if (!isLoading && !session) {
      router.push("/sign-in");
    }
  }, [session, isLoading, router]);

  useEffect(() => {
    async function fetchTasks() {
      if (!session || !user) return;

      try {
        const token = (session as any).token || "";
        const userTasks = await getTasks(user.id, token);
        setTasks(userTasks);
      } catch (err: any) {
        setError(err.message || "Failed to load tasks");
      } finally {
        setTasksLoading(false);
      }
    }

    if (session && user) {
      fetchTasks();
    }
  }, [session, user]);

  async function handleTaskUpdated() {
    if (!session || !user) return;

    try {
      const token = (session as any).token || "";
      const userTasks = await getTasks(user.id, token);
      setTasks(userTasks);
    } catch (err: any) {
      console.error("Failed to refresh tasks:", err);
    }
  }

  async function handleTaskDeleted() {
    await handleTaskUpdated();
  }

  async function handleSignOut() {
    await signOut();
    router.push("/sign-in");
  }

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
    <div className="min-h-screen relative flex overflow-hidden">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-screen lg:ml-64">
        {/* Background Image with Overlay */}
        <div className="fixed inset-0 z-0">
          <div
            className="absolute inset-0 bg-cover bg-center bg-no-repeat"
            style={{ backgroundImage: "url('/images/task12.webp')" }}
          />
          <div className="absolute inset-0 bg-gradient-to-br from-violet-600/75 via-purple-600/75 to-pink-600/75" />
        </div>

        {/* Header */}
        <header className="bg-gradient-to-r from-purple-300/95 via-pink-300/95 to-purple-300/95 backdrop-blur-sm shadow-lg border-b border-purple-400/70 relative z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 rounded-lg hover:bg-purple-200 transition-colors"
              >
                <svg className="w-6 h-6 text-purple-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl flex items-center justify-center shadow-lg">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                </svg>
              </div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-900 to-pink-900 bg-clip-text text-transparent">TaskMaster</h1>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-purple-950">{user.email}</p>
              </div>
              <button
                onClick={() => router.push("/chat")}
                className="hidden sm:flex px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg hover:from-blue-600 hover:to-purple-600 transition-all shadow-md hover:shadow-lg items-center gap-2 font-medium"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                AI Chat
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

        {/* Welcome Section */}
        <div className="bg-white/10 backdrop-blur-md text-white shadow-xl border-b border-white/20 relative z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
            <h2 className="text-3xl md:text-4xl font-bold mb-2 drop-shadow-lg">Welcome to Your Task Records</h2>
            <p className="text-white/90 text-lg drop-shadow">Organize, track, and accomplish your goals efficiently</p>
          </div>
        </div>

        {/* Main content */}
        <main className="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 flex-grow relative z-10">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl mb-4">
              {error}
            </div>
          )}

          {tasksLoading ? (
            <div className="bg-white rounded-2xl shadow-lg p-8 text-center">
              <div className="text-gray-500">Loading tasks...</div>
            </div>
          ) : (
            <TaskList
              tasks={tasks}
              onTaskUpdated={handleTaskUpdated}
              onTaskDeleted={handleTaskDeleted}
            />
          )}
        </main>

        {/* Footer */}
        <footer className="bg-gradient-to-r from-purple-300/95 via-pink-300/95 to-purple-300/95 backdrop-blur-sm border-t border-purple-400/70 mt-auto shadow-lg relative z-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
              <div className="text-center md:text-left">
                <p className="text-purple-950 font-semibold">Made with ❤️ by Bilqees Shahid</p>
                <p className="text-sm text-purple-800 mt-1">© {new Date().getFullYear()} All rights reserved</p>
              </div>
              <div className="flex items-center gap-2 text-purple-900">
                <svg className="w-5 h-5 text-purple-800" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
                <span className="text-sm font-medium">TaskMaster Pro</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
