from fastapi import APIRouter, Response, status, Depends, HTTPException, Form
from sqlmodel import Session, select
from app.core.db import db_session
from app.models.users import User
from app.api.utils.users_auth_utils import Auth , get_user_auth

user_router = APIRouter(prefix="/users", tags=["users"])



@user_router.post("/signup", status_code= status.HTTP_201_CREATED)
async def create_new_user(user_data: User, user_auth: Auth= Depends(get_user_auth)): #called Action


    if not user_data.first_name or not user_data.email or not user_data.user_name or not user_data.last_name or not user_data.password:
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Required fields")
    
    #for username confirmation
    user_name = await user_auth.get_user_by_useranme(user_data.user_name)
    if user_name:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="username exists, create new account")
    
    #for email verification by get_user_email
    user = await user_auth.get_user_by_email(user_data.email)
    if user:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="email exists, create new account")
    print(f"user generated password {user_data.password}")
    hashed_password = user_auth.hash_password(user_data.password)
    user_data.password  = hashed_password
    print(f"user with hashed password { user_data}")


    data = user_data

    user_auth.db_session.add(data)
    user_auth.db_session.commit()
    user_auth.db_session.refresh(data)

    if data is None:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")
    return {"status": True, "Message": "user created successfully", "user_data": data}


@user_router.post("/signin")
async def sign_in(response: Response, user_email: str = Form(...), user_password: str = Form(...), user_auth: Auth = Depends(get_user_auth)):
    is_user_exist = await user_auth.get_user_by_email(user_email)  # Removed await
    if not is_user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    is_password_match = user_auth.verify_password(user_password, is_user_exist.password)
    if not is_password_match:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    user_id = is_user_exist.id
    access_token, refresh_token = user_auth.create_tokens(user_id)

    response.set_cookie(
        key="inventory_refresh_token",
        value=refresh_token,
        httponly=False,
        secure=True,
        samesite="Strict"  # Fixed typo
    )

    return {"status": True, "message": "You are logged in successfully", "access_token": access_token, "user": is_user_exist}
