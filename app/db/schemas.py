from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# User Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserOut(UserInDB):
    pass

# Book Schema
class BookBase(BaseModel):
    title: str
    author: str
    pub_date: date
    l_code: int

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookInDB(BookBase):
    id: int

    class Config:
        orm_mode = True

class BookOut(BookInDB):
    pass

# Borrow Schema
class BorrowBase(BaseModel):
    book_id: int
    student_id: int
    date_of_borrow: date
    return_time: Optional[date] = None

class BorrowCreate(BorrowBase):
    pass

class BorrowUpdate(BorrowBase):
    pass

class BorrowInDB(BorrowBase):
    id: int

    class Config:
        orm_mode = True

class BorrowOut(BorrowInDB):
    pass

# College Schema
class CollegeBase(BaseModel):
    name: str
    office: int
    phone: str
    dean: int
    apikey: str

class CollegeCreate(CollegeBase):
    pass

class CollegeUpdate(CollegeBase):
    pass

class CollegeInDB(CollegeBase):
    id: int

    class Config:
        orm_mode = True

class CollegeOut(CollegeInDB):
    pass

# Course Schema
class CourseBase(BaseModel):
    name: str
    level: str
    description: str
    dept_code: int
    credit: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseInDB(CourseBase):
    code: int

    class Config:
        orm_mode = True

class CourseOut(CourseInDB):
    pass

# Delete Schema
class DeleteBase(BaseModel):
    student_id: int
    section_id: int
    type: int
    date_of_deletion: date

class DeleteCreate(DeleteBase):
    pass

class DeleteUpdate(DeleteBase):
    pass

class DeleteInDB(DeleteBase):
    id: int

    class Config:
        orm_mode = True

class DeleteOut(DeleteInDB):
    pass

# Dept Schema
class DeptBase(BaseModel):
    name: str
    office: int
    phone: str
    college_id: int

class DeptCreate(DeptBase):
    pass

class DeptUpdate(DeptBase):
    pass

class DeptInDB(DeptBase):
    code: int

    class Config:
        orm_mode = True

class DeptOut(DeptInDB):
    pass

# EducationalEmployee Schema
class EducationalEmployeeBase(BaseModel):
    degree: int
    edu_id: int
    apikey: str

class EducationalEmployeeCreate(EducationalEmployeeBase):
    pass

class EducationalEmployeeUpdate(EducationalEmployeeBase):
    pass

class EducationalEmployeeInDB(EducationalEmployeeBase):
    id: int

    class Config:
        orm_mode = True

class EducationalEmployeeOut(EducationalEmployeeInDB):
    pass

# Employee Schema
class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    position: str
    salary: int
    department_id: int

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class EmployeeInDB(EmployeeBase):
    id: int

    class Config:
        orm_mode = True

class EmployeeOut(EmployeeInDB):
    pass

# Grade Schema
class GradeBase(BaseModel):
    student_id: int
    section_id: int
    grade: int

class GradeCreate(GradeBase):
    pass

class GradeUpdate(GradeBase):
    pass

class GradeInDB(GradeBase):
    id: int

    class Config:
        orm_mode = True

class GradeOut(GradeInDB):
    pass

# Professor Schema
class ProfessorBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    department_id: int

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorUpdate(ProfessorBase):
    pass

class ProfessorInDB(ProfessorBase):
    id: int

    class Config:
        orm_mode = True

class ProfessorOut(ProfessorInDB):
    pass

# Room Schema
class RoomBase(BaseModel):
    location: str
    capacity: int

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomInDB(RoomBase):
    code: int

    class Config:
        orm_mode = True

class RoomOut(RoomInDB):
    pass

# Section Schema
class SectionBase(BaseModel):
    year: int
    semester: str
    room_code: int
    course_code: int
    professor_id: int

class SectionCreate(SectionBase):
    pass

class SectionUpdate(SectionBase):
    pass

class SectionInDB(SectionBase):
    id: int

    class Config:
        orm_mode = True

class SectionOut(SectionInDB):
    pass

# Student Schema
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    address: str
    dept_code: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentInDB(StudentBase):
    id: int

    class Config:
        orm_mode = True

class StudentOut(StudentInDB):
    pass

# Takes Schema
class TakesBase(BaseModel):
    student_id: int
    course_code: int
    year: int
    semester: str

class TakesCreate(TakesBase):
    pass

class TakesUpdate(TakesBase):
    pass

class TakesInDB(TakesBase):
    id: int

    class Config:
        orm_mode = True

class TakesOut(TakesInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None