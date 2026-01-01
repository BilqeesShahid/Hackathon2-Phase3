/*Auth context provider for Next.js frontend.*/
"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface AuthContextType {
  user: User | null;
  session: Session | null;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<{ success: boolean; error?: string }>;
  signUp: (email: string, password: string, name?: string) => Promise<{ success: boolean; error?: string }>;
  signOut: () => Promise<void>;
}

interface User {
  id: string;
  email: string;
  name: string | null;
  image: string | null;
}

interface Session {
  user: User;
  token: string;
  expiresAt: number;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkSession();
  }, []);

  async function checkSession() {
    const token = localStorage.getItem("auth_token");
    if (!token) {
      setIsLoading(false);
      return;
    }
    try {
      const response = await fetch(API_URL + "/auth/verify", {
        method: "GET",
        headers: { Authorization: "Bearer " + token },
      });
      if (response.ok) {
        const result = await response.json();
        setUser({ id: result.user_id, email: result.email, name: null, image: null });
        setSession({ user: { id: result.user_id, email: result.email, name: null, image: null }, token, expiresAt: 0 });
      }
    } catch (error) {
      console.error("Failed to get session:", error);
    } finally {
      setIsLoading(false);
    }
  }

  async function signIn(email: string, password: string) {
    try {
      const response = await fetch(API_URL + "/auth/sign-in", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const result = await response.json();
      if (response.ok && result.token) {
        localStorage.setItem("auth_token", result.token);
        setUser({ id: result.user_id, email: result.email, name: null, image: null });
        setSession({ user: { id: result.user_id, email: result.email, name: null, image: null }, token: result.token, expiresAt: 0 });
        return { success: true };
      }
      return { success: false, error: result.detail || "Invalid credentials" };
    } catch (error: any) {
      console.error("Sign in error:", error);
      return { success: false, error: error.message || "Sign in failed" };
    }
  }

  async function signUp(email: string, password: string, name?: string) {
    try {
      const response = await fetch(API_URL + "/auth/sign-up", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, name }),
      });
      const result = await response.json();
      if (response.ok && result.token) {
        localStorage.setItem("auth_token", result.token);
        setUser({ id: result.user_id, email: result.email, name: name || null, image: null });
        setSession({ user: { id: result.user_id, email: result.email, name: name || null, image: null }, token: result.token, expiresAt: 0 });
        return { success: true };
      }
      return { success: false, error: result.detail || "Sign up failed" };
    } catch (error: any) {
      console.error("Sign up error:", error);
      return { success: false, error: error.message || "Sign up failed" };
    }
  }

  async function signOut() {
    localStorage.removeItem("auth_token");
    setSession(null);
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        session,
        isLoading,
        signIn,
        signUp,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
