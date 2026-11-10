from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.department import Department
from schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
    DepartmentUpdate,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/departments", tags=["Departments"])


# 1. Create Department
@router.post("/", response_model=DepartmentResponse)
def create_department(dept: DepartmentCreate, db: Session = Depends(get_db)):
  db_dept = Department(name=dept.name, code=dept.code)
  db.add(db_dept)
  db.commit()
  db.refresh(db_dept)
  return db_dept


# 2. Get All Departments
@router.get("/", response_model=list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
  return db.query(Department).all()


# 3. Get Single Department by ID
@router.get("/{dept_id}", response_model=DepartmentResponse)
def get_department(dept_id: int, db: Session = Depends(get_db)):
  dept = db.query(Department).filter(Department.id == dept_id).first()
  if not dept:
    raise HTTPException(status_code=404, detail="Department not found")
  return dept


# 4. Update Department
@router.put("/{dept_id}", response_model=DepartmentResponse)
def update_department(
    dept_id: int, dept_update: DepartmentUpdate, db: Session = Depends(get_db)
):
  dept = db.query(Department).filter(Department.id == dept_id).first()
  if not dept:
    raise HTTPException(status_code=404, detail="Department not found")

  if dept_update.name is not None:
    dept.name = dept_update.name
  if dept_update.code is not None:
    dept.code = dept_update.code

  db.commit()
  db.refresh(dept)
  return dept


# 5. Delete Department
@router.delete("/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db)):
  dept = db.query(Department).filter(Department.id == dept_id).first()
  if not dept:
    raise HTTPException(status_code=404, detail="Department not found")
  db.delete(dept)
  db.commit()
  return {"message": "Department deleted successfully"}