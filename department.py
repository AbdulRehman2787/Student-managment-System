from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Department(Base):
  __tablename__ = "departments"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, unique=True, index=True)
  code = Column(String, unique=True, index=True)

  students = relationship("Student", back_populates="department")
  teachers = relationship("Teacher", back_populates="department")
  courses = relationship("Course", back_populates="department")