from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.course import Course
from models.student import Student
from schemas.course import CourseCreate, CourseResponse, CourseUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/courses", tags=["Courses"])


# 1. Create Course
@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
  db_course = Course(
      title=course.title,
      department_id=course.department_id,
      teacher_id=course.teacher_id,
  )
  db.add(db_course)
  db.commit()
  db.refresh(db_course)
  return db_course


# 2. Get All Courses
@router.get("/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
  return db.query(Course).all()


# 3. Get Single Course by ID
@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
  course = db.query(Course).filter(Course.id == course_id).first()
  if not course:
    raise HTTPException(status_code=404, detail="Course not found")
  return course


# 4. Enroll Student in Course
@router.post("/{course_id}/enroll/{student_id}")
def enroll_student(course_id: int, student_id: int, db: Session = Depends(get_db)):
  course = db.query(Course).filter(Course.id == course_id).first()
  student = db.query(Student).filter(Student.id == student_id).first()

  if not course or not student:
    raise HTTPException(status_code=404, detail="Course or Student not found")

  if student not in course.students:
    course.students.append(student)
    db.commit()

  return {"message": f"Student {student_id} enrolled in course {course_id}"}


# 5. Update Course
@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)
):
  course = db.query(Course).filter(Course.id == course_id).first()
  if not course:
    raise HTTPException(status_code=404, detail="Course not found")

  if course_update.title is not None:
    course.title = course_update.title
  if course_update.department_id is not None:
    course.department_id = course_update.department_id
  if course_update.teacher_id is not None:
    course.teacher_id = course_update.teacher_id

  db.commit()
  db.refresh(course)
  return course


# 6. Delete Course
@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
  course = db.query(Course).filter(Course.id == course_id).first()
  if not course:
    raise HTTPException(status_code=404, detail="Course not found")
  db.delete(course)
  db.commit()
  return {"message": "Course deleted successfully"}