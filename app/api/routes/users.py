from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from app.core.db import db_session
from app.models.users import User

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/", status_code= status.HTTP_201_CREATED)
async def create_new_user(user_data: User, session: Session= Depends(db_session)): #called Action
    if not user_data.first_name or not user_data.email or not user_data.user_name or not user_data.last_name or not user_data.password:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Required fields")
    
    #for username confirmation
    statement = select(User).where(User.user_name==user_data.user_name)
    isusernameexist = session.exec(statement).first()
    if isusernameexist:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="username exist, crate new account")
    
    #for email verification
    statement = select(User).where(User.email==user_data.email)
    isemailexist = session.exec(statement).first()
    if isemailexist:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="email exist, create new account")
    
    data = user_data


    session.add(data)
    session.commit()
    session.refresh(data)

    if data is None:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")
    return {"status": True, "Message": "user created successfully", "user_data": data}