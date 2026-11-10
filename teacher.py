from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.teacher import Teacher
from schemas.teacher import TeacherCreate, TeacherResponse, TeacherUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/teachers", tags=["Teachers"])


# 1. Create Teacher
@router.post("/", response_model=TeacherResponse)
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
  db_teacher = Teacher(
      name=teacher.name,
      email=teacher.email,
      department_id=teacher.department_id,
  )
  db.add(db_teacher)
  db.commit()
  db.refresh(db_teacher)
  return db_teacher


# 2. Get All Teachers
@router.get("/", response_model=list[TeacherResponse])
def get_teachers(db: Session = Depends(get_db)):
  return db.query(Teacher).all()


# 3. Get Single Teacher by ID
@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
  teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
  if not teacher:
    raise HTTPException(status_code=404, detail="Teacher not found")
  return teacher


# 4. Update Teacher
@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(
    teacher_id: int, teacher_update: TeacherUpdate, db: Session = Depends(get_db)
):
  teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
  if not teacher:
    raise HTTPException(status_code=404, detail="Teacher not found")

  if teacher_update.name is not None:
    teacher.name = teacher_update.name
  if teacher_update.email is not None:
    teacher.email = teacher_update.email
  if teacher_update.department_id is not None:
    teacher.department_id = teacher_update.department_id

  db.commit()
  db.refresh(teacher)
  return teacher


# 5. Delete Teacher
@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
  teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
  if not teacher:
    raise HTTPException(status_code=404, detail="Teacher not found")
  db.delete(teacher)
  db.commit()
  return {"message": "Teacher deleted successfully"}