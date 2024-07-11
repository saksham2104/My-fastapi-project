from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import bcrypt

security = HTTPBasic()

plain_password = "10112004"
hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "Saksham"
    
    if credentials.username != correct_username or not bcrypt.checkpw(credentials.password.encode('utf-8'), hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
