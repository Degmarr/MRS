from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# SQLAlchemy setup
DATABASE_URL = "sqlite:///./medical.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
templates = Jinja2Templates(directory="templates")

# Define CombinedModel


class CombinedModel(Base):
    __tablename__ = "combined_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    address = Column(String)
    national_id = Column(String, unique=True, index=True)
    diagnosis = Column(String)
    treatment = Column(Text)
    allergies = Column(String)
    immunizations = Column(String)
    family_history = Column(Text)


# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI setup
app = FastAPI()

# Mounting the static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates setup
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",  # Add the URL of your frontend
    # Add other origins as needed
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request


class CombinedDataCreate(BaseModel):
    name: str
    age: int
    address: str
    national_id: str
    diagnosis: str
    treatment: str
    allergies: str
    immunizations: str
    family_history: str

# CRUD operations


@app.post("/combined_data/", response_model=CombinedDataCreate)
def create_combined_data(data: CombinedDataCreate, db: Session = Depends(get_db)):
    db_data = CombinedModel(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


@app.get("/combined_data/{national_id}", response_model=CombinedDataCreate)
def read_combined_data(national_id: str, db: Session = Depends(get_db)):
    db_data = db.query(CombinedModel).filter(
        CombinedModel.national_id == national_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return db_data


@app.put("/combined_data/{national_id}", response_model=CombinedDataCreate)
def update_combined_data(national_id: str, data: CombinedDataCreate, db: Session = Depends(get_db)):
    db_data = db.query(CombinedModel).filter(
        CombinedModel.national_id == national_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    for key, value in data.dict().items():
        setattr(db_data, key, value)
    db.commit()
    db.refresh(db_data)
    return db_data


@app.delete("/combined_data/{national_id}", response_model=dict)
def delete_combined_data(national_id: str, db: Session = Depends(get_db)):
    print(f"Deleting record with national_id: {national_id}")
    db_data = db.query(CombinedModel).filter(
        CombinedModel.national_id == national_id).first()
    if db_data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    db.delete(db_data)
    db.commit()
    return {"message": "Data deleted successfully"}


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/add", response_class=HTMLResponse)
async def read_add_data(request: Request):
    return templates.TemplateResponse("add_data.html", {"request": request})


@app.get("/combined_data/", response_model=list[CombinedDataCreate])
def get_combined_data(db: Session = Depends(get_db)):
    db_data = db.query(CombinedModel).all()
    return db_data
