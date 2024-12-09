from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import User, Task
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user_id/tasks")
def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks


@router.get("/user_id")
def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User was not found")


@router.post("/create")
def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    new_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.username)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update")
def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if existing_user is not None:
        existing_user.firstname = user.firstname
        existing_user.lastname = user.lastname
        existing_user.age = user.age
        db.commit()
        db.refresh(existing_user)
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
    else:
        raise HTTPException(status_code=404, detail="User was not found")


@router.delete("/delete")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if existing_user is not None:
        tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
        for task in tasks:
            db.delete(task)
        db.delete(existing_user)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User and tasks deleted successfully!'}
    else:
        raise HTTPException(status_code=404, detail="User was not found")


"""@router.delete("/delete")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if existing_user is not None:
        db.delete(existing_user)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted successfully!'}
    else:
        raise HTTPException(status_code=404, detail="User was not found")"""