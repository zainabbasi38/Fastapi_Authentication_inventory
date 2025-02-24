from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlmodel import Session
from app.core.db import db_session
from app.models.products import Product
from app.api.utils.users_auth_utils import get_user_auth

product_router = APIRouter(prefix="/products" , tags= ["products"])

@product_router.post("/")
async def create_product(product:Product,authorization:str= Header(...), session:Session= Depends(get_user_auth)):
   
   if not authorization.startswith("Bearer "):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Unauthorized")
   
   token = authorization.split(" ")[1]

   istokenverified = session.verify_token(token)
   print(istokenverified)

   if not istokenverified:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"{istokenverified}")
   
   return {"status": True, "message": "Product created successfully", "data":istokenverified["sub"]}
   
   
   