from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.student import Student
from schemas.student import StudentCreate, StudentResponse, StudentUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/students", tags=["Students"])


# 1. Create Student
@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
  db_student = Student(
      name=student.name,
      email=student.email,
      department_id=student.department_id,
  )
  db.add(db_student)
  db.commit()
  db.refresh(db_student)
  return db_student


# 2. Get All Students
@router.get("/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
  return db.query(Student).all()


# 3. Get Single Student by ID
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
  student = db.query(Student).filter(Student.id == student_id).first()
  if not student:
    raise HTTPException(status_code=404, detail="Student not found")
  return student


# 4. Update Student
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)
):
  student = db.query(Student).filter(Student.id == student_id).first()
  if not student:
    raise HTTPException(status_code=404, detail="Student not found")

  if student_update.name is not None:
    student.name = student_update.name
  if student_update.email is not None:
    student.email = student_update.email
  if student_update.department_id is not None:
    student.department_id = student_update.department_id

  db.commit()
  db.refresh(student)
  return student


# 5. Delete Student
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
  student = db.query(Student).filter(Student.id == student_id).first()
  if not student:
    raise HTTPException(status_code=404, detail="Student not found")
  db.delete(student)
  db.commit()
  return {"message": "Student deleted successfully"}