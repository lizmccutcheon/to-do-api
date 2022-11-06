from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    firstname = Column(String(40))
    lastname = Column(String(40), index=True)
    email = Column(String(50), index=True)

    tasks = relationship("PersonHasTask", back_populates="person")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    short_name = Column(String)
    description = Column(String(255))

    people = relationship("PersonHasTask", back_populates="task")


class PersonHasTask(Base):
    __tablename__ = "people_have_tasks"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    person_id = Column(Integer, ForeignKey("people.id"))
    completed = Column(Boolean)

    person = relationship("Person", back_populates="tasks")
    task = relationship("Task", back_populates="people")
