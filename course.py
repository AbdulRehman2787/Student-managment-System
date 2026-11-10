from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

# Association table direct yahin define hai
student_courses = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)


class Course(Base):
  __tablename__ = "courses"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  department_id = Column(Integer, ForeignKey("departments.id"))
  teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)

  department = relationship("Department", back_populates="courses")
  teacher = relationship("Teacher", back_populates="courses")
  students = relationship(
      "Student", secondary=student_courses, back_populates="courses"
  )