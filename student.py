from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Student(Base):
  __tablename__ = "students"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  email = Column(String, unique=True, index=True)
  department_id = Column(Integer, ForeignKey("departments.id"))

  department = relationship("Department", back_populates="students")
  courses = relationship(
      "Course", secondary="student_courses", back_populates="students"
  )