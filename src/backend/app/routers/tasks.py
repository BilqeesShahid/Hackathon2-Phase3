"""Task router for Phase II Todo Application."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.middleware.auth import get_current_user, verify_user_access, CurrentUser
from app.db.config import get_session
from sqlmodel import Session

router = APIRouter(prefix="/api", tags=["Tasks"])


def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    """Dependency for getting TaskService instance."""
    return TaskService(session)


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    current_user: CurrentUser = Depends(get_current_user),
    verified_user_id: str = Depends(verify_user_access),
    service: TaskService = Depends(get_task_service),
):
    """List all tasks for the authenticated user."""
    return service.get_by_user(verified_user_id)


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: CurrentUser = Depends(get_current_user),
    verified_user_id: str = Depends(verify_user_access),
    service: TaskService = Depends(get_task_service),
):
    """Create a new task for the authenticated user."""
    return service.create(
        user_id=verified_user_id,
        title=task_data.title,
        description=task_data.description,
    )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    verified_user_id: str = Depends(verify_user_access),
    service: TaskService = Depends(get_task_service),
):
    """Get a specific task by ID."""
    task = service.get_by_id(task_id, verified_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    verified_user_id: str = Depends(verify_user_access),
    service: TaskService = Depends(get_task_service),
):
    """Update a task's title or description."""
    task = service.update(
        task_id=task_id,
        user_id=verified_user_id,
        title=task_data.title,
        description=task_data.description,
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    verified_user_id: str = Depends(verify_user_access),
    service: TaskService = Depends(get_task_service),
):
    """Delete a task."""
    success = service.delete(task_id, verified_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    verified_user_id: str = Depends(verify_user_access),
    service: TaskService = Depends(get_task_service),
):
    """Toggle task completion status."""
    task = service.toggle_complete(task_id, verified_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task
