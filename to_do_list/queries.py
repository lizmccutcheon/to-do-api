from sqlalchemy.orm import Session

from .models import Person, Task  # , PersonHasTask
from . import schemas as s


def get_person_by_id(db: Session, id: int):
    return db.query(Person).filter(Person.id == id).first()


def get_person_by_email(db: Session, email: str):
    return db.query(Person).filter(Person.email == email).first()


def get_people(db: Session):
    return db.query(Person).order_by(Person.lastname, Person.firstname).all()


def create_person(db: Session, person: s.PersonCreate):
    new_person = Person(
        firstname=person.firstname, lastname=person.lastname, email=person.email
    )
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


def get_task_by_id(db: Session, id: int):
    return db.query(Task).filter(Task.id == id).first()


def get_tasks(db: Session):
    return db.query(Task).order_by(Task.title).all()


def create_task(db: Session, task: s.TaskCreate):
    new_task = Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_tasks(db: Session):
    return db.query(Task).all()
