from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from starlette.requests import Request
import bcrypt

app = FastAPI()

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

DATABASE_URL = "postgresql://postgres:saksham%402@localhost:5432/names"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

security = HTTPBasic()

# Password hashing 
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

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test-db-connection")
async def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text('SELECT 1')).fetchone()
        return {"message": "Database connection successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    result = db.execute(text('SELECT * FROM "Table"')).fetchall()
    data = [{"id": row[0], "name": row[1]} for row in result]
    return templates.TemplateResponse("display.html", {"request": request, "data": data, "username": current_user})

@app.get("/data")
async def get_data(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    result = db.execute(text('SELECT * FROM "Table"')).fetchall()
    return {"data": [{"id": row[0], "name": row[1]} for row in result]}

@app.get("/display", response_class=HTMLResponse)
async def display_html():
    return FileResponse("templates/display.html")
