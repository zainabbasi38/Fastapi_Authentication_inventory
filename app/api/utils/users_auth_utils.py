from datetime import datetime, timedelta, timezone
from typing import Union
import bcrypt
import jwt
from sqlmodel import Session, select
from fastapi import Depends
from app.core.db import db_session
from app.models.users import User


class Auth():
    access_token_key = "gfjdftydfytdff"
    refresh_token_key = "gfjdfjkguufuifuiftydfytdff"
    def __init__(self, db_session : Session = Depends(db_session)):
        self.db_session = db_session

    async def get_user_by_email(self, email: str)->Union[User, None]:
        print("Email come ", email)

        #transformation of data to run validation
        email_in_lowercase = email.lower()
        statement = select(User).where(User.email == email_in_lowercase)
        #return ->> True or false but it depends on return data
        isemailexist = self.db_session.exec(statement).first()
        return isemailexist
    
    async def get_user_by_id(self, id: str)->Union[User, None]:

        #transformation of data to run validation
    
        statement = select(User).where(User.email == id)
        #return ->> True or false but it depends on return data
        isidexist = self.db_session.exec(statement).first()
        return isidexist
    
    async def get_user_by_useranme(self, user_name: str)->Union[User, None]:

        #transformation of data to run validation
    
        statement = select(User).where(User.user_name == user_name)
        #return ->> True or false but it depends on return data
        isusernameexist = self.db_session.exec(statement).first()
        return isusernameexist

    @staticmethod
    def hash_password(password: str) -> str:
        # use bcrypt to hash password
        # saltvalue = 10 
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    @staticmethod
    def verify_password(password:str, hashed_password: str) -> bool:
        is_password_match = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        return is_password_match
    #Assumptions
    #programmer or coder must write assumptions
    #create tokens access, refresh tokens
    #user id
    #create access and refresh tokens with JWT
    #issue date,, expiry date
    #return access tokens and refresh tokens in tuple

    def create_tokens(self,user_id:str)->tuple[str, str]:
        issued_at = datetime.now(timezone.utc)
        access_token_expired_at = datetime.now(timezone.utc) + timedelta(hours=3)
        refresh_token_expired_at = datetime.now(timezone.utc) + timedelta(days=7)
        #create acccess tokens
        access_token= jwt.encode(
            {"sub": str(user_id), "exp": access_token_expired_at, "iat": issued_at},
            self.access_token_key,
            algorithm='HS256'
        )
        #create refresh token
        refresh_token= jwt.encode(
            {"sub": str(user_id), "exp": refresh_token_expired_at, "iat": issued_at},
            self.refresh_token_key,
            algorithm='HS256'
        )

        return access_token, refresh_token
    
    def verify_token(self, token: str, token_type: str = "access")->str:
        try:
            key = self.access_token_key if token_type == "access" else self.refresh_token_key
            verified_token = jwt.decode(token, key , algorithms=["HS256"])
            return verified_token
        except jwt.ExpiredSignatureError:
            print("You session has expired, please login again")
            return "You session has expired, please login again"

        except jwt.InvalidTokenError:
            print("Invalid token")
            return "Invalid token"


def get_user_auth(db_sesion : Session= Depends(db_session))->Auth:
    return Auth(db_sesion)
# user_auth = Auth()
        
#is classs is callable = yes
# is object is callable = No