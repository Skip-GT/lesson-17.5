from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import Task, User
from schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get("/task_id")
def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task is not None:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task was not found")


@router.post("/create")
def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user is not None:
        new_task = Task(
            title=task.title,
            content=task.content,
            priority=task.priority,
            user_id=user_id,
            slug=task.title
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
    else:
        raise HTTPException(status_code=404, detail="User was not found")


@router.put("/update")
def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    existing_task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if existing_task is not None:
        existing_task.title = task.title
        existing_task.content = task.content
        existing_task.priority = task.priority
        db.commit()
        db.refresh(existing_task)
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}
    else:
        raise HTTPException(status_code=404, detail="Task was not found")


@router.delete("/delete")
def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if existing_task is not None:
        db.delete(existing_task)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deleted successfully!'}
    else:
        raise HTTPException(status_code=404, detail="Task was not found")
