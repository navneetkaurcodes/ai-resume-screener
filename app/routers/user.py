from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import (UserCreate,UserResponse)
from app.core.security import hash_password

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/create_user",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = (db.query(User).filter(User.email == user.email).first())

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered")

    new_user = User(email=user.email,hashed_password=hash_password(user.password),full_name=user.full_name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/display_users",response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/display_user/{user_id}",response_model=UserResponse)
def get_user(user_id: int,db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.id == user_id).first())

    if not user:
        raise HTTPException(status_code=404,detail="User not found")

    return user

@router.put("/update_user/{user_id}", response_model=UserResponse)
def update_user(user_id: int,updated_user: UserCreate,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")

    user.email = updated_user.email
    user.full_name = updated_user.full_name
    user.hashed_password = updated_user.password  # : Hash password later

    db.commit()
    db.refresh(user)

    return user

@router.delete("/delete_user/{user_id}")
def delete_user(user_id: int,db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404,detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
