/*API client utility with authentication for Phase II Todo Application.*/
import axios, { AxiosInstance, AxiosError } from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Create an authenticated API client.
 * The auth token should be set separately via setAuthToken.
 */
export function createApiClient(token?: string): AxiosInstance {
  return axios.create({
    baseURL: API_URL,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });
}

/**
 * API error response structure
 */
export interface ApiError {
  detail: string;
}

/**
 * Task response from API
 */
export interface TaskResponse {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Create task request
 */
export interface TaskCreate {
  title: string;
  description?: string;
}

/**
 * Update task request
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
}

/**
 * Get tasks for a user
 */
export async function getTasks(
  userId: string,
  token: string
): Promise<TaskResponse[]> {
  const api = createApiClient(token);
  const response = await api.get<TaskResponse[]>(`/api/${userId}/tasks`);
  return response.data;
}

/**
 * Create a new task
 */
export async function createTask(
  userId: string,
  data: TaskCreate,
  token: string
): Promise<TaskResponse> {
  const api = createApiClient(token);
  const response = await api.post<TaskResponse>(`/api/${userId}/tasks`, data);
  return response.data;
}

/**
 * Update a task
 */
export async function updateTask(
  userId: string,
  taskId: number,
  data: TaskUpdate,
  token: string
): Promise<TaskResponse> {
  const api = createApiClient(token);
  const response = await api.put<TaskResponse>(
    `/api/${userId}/tasks/${taskId}`,
    data
  );
  return response.data;
}

/**
 * Delete a task
 */
export async function deleteTask(
  userId: string,
  taskId: number,
  token: string
): Promise<void> {
  const api = createApiClient(token);
  await api.delete(`/api/${userId}/tasks/${taskId}`);
}

/**
 * Toggle task completion status
 */
export async function toggleComplete(
  userId: string,
  taskId: number,
  token: string
): Promise<TaskResponse> {
  const api = createApiClient(token);
  const response = await api.patch<TaskResponse>(
    `/api/${userId}/tasks/${taskId}/complete`
  );
  return response.data;
}
