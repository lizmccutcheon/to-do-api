from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import schemas as s, queries as q
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/people/", response_model=list[s.Person])
def get_people(db: Session = Depends(get_db)):
    return q.get_people(db)


@app.post("/people/", response_model=s.Person)
def create_person(person: s.PersonCreate, db: Session = Depends(get_db)):
    check_person = q.get_person_by_email(db, email=person.email)
    if check_person:
        raise HTTPException(status_code=400, detail="Email already taken")
    return q.create_person(db, person=person)


@app.get("/people/{person_id}", response_model=s.Person)
def get_person_by_id(person_id: int, db: Session = Depends(get_db)):
    person = q.get_person_by_id(db, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="No such person")
    return person


@app.get("/tasks/", response_model=list[s.Task])
def get_tasks(db: Session = Depends(get_db)):
    return q.get_tasks(db)


@app.post("/tasks/", response_model=s.Task)
def create_task(task: s.TaskCreate, db: Session = Depends(get_db)):
    return q.create_task(db, task=task)


@app.get("/tasks/{task_id}", response_model=s.Task)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = q.get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="No such task")
    return task
