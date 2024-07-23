from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password, role="student"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

# Book CRUD operations
def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_book(db: Session, book: models.Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def update_book(db: Session, book_id: int, title: str = None, author: str = None, pub_date: str = None, l_code: int = None):
    book = get_book(db, book_id)
    if book:
        if title:
            book.title = title
        if author:
            book.author = author
        if pub_date:
            book.pub_date = pub_date
        if l_code:
            book.l_code = l_code
        db.commit()
        db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
    return book

# Borrow CRUD operations
def get_borrows(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Borrow).offset(skip).limit(limit).all()

def create_borrow(db: Session, borrow: models.Borrow):
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow

def update_borrow(db: Session, borrow_id: int, date_of_borrow: str = None, return_time: str = None):
    borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if borrow:
        if date_of_borrow:
            borrow.date_of_borrow = date_of_borrow
        if return_time:
            borrow.return_time = return_time
        db.commit()
        db.refresh(borrow)
    return borrow

def delete_borrow(db: Session, borrow_id: int):
    borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
    if borrow:
        db.delete(borrow)
        db.commit()
    return borrow

# College CRUD operations
def get_colleges(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.College).offset(skip).limit(limit).all()

def get_college(db: Session, college_id: int):
    return db.query(models.College).filter(models.College.id == college_id).first()

def create_college(db: Session, college: models.College):
    db.add(college)
    db.commit()
    db.refresh(college)
    return college

def update_college(db: Session, college_id: int, name: str = None, office: int = None, phone: str = None, dean: int = None, apikey: str = None):
    college = get_college(db, college_id)
    if college:
        if name:
            college.name = name
        if office:
            college.office = office
        if phone:
            college.phone = phone
        if dean:
            college.dean = dean
        if apikey:
            college.apikey = apikey
        db.commit()
        db.refresh(college)
    return college

def delete_college(db: Session, college_id: int):
    college = get_college(db, college_id)
    if college:
        db.delete(college)
        db.commit()
    return college

# CollegeDept CRUD operations
def get_college_depts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.CollegeDept).offset(skip).limit(limit).all()

def create_college_dept(db: Session, college_dept: models.CollegeDept):
    db.add(college_dept)
    db.commit()
    db.refresh(college_dept)
    return college_dept

def delete_college_dept(db: Session, college_id: int, dept_code: int):
    college_dept = db.query(models.CollegeDept).filter(models.CollegeDept.college_id == college_id, models.CollegeDept.dept_code == dept_code).first()
    if college_dept:
        db.delete(college_dept)
        db.commit()
    return college_dept

# Course CRUD operations
def get_courses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Course).offset(skip).limit(limit).all()

def get_course(db: Session, course_code: int):
    return db.query(models.Course).filter(models.Course.code == course_code).first()

def create_course(db: Session, course: models.Course):
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def update_course(db: Session, course_code: int, name: str = None, level: str = None, description: str = None, dept_code: int = None, credit: int = None):
    course = get_course(db, course_code)
    if course:
        if name:
            course.name = name
        if level:
            course.level = level
        if description:
            course.description = description
        if dept_code:
            course.dept_code = dept_code
        if credit:
            course.credit = credit
        db.commit()
        db.refresh(course)
    return course

def delete_course(db: Session, course_code: int):
    course = get_course(db, course_code)
    if course:
        db.delete(course)
        db.commit()
    return course

# Delete CRUD operations
def get_deletes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Delete).offset(skip).limit(limit).all()

def create_delete(db: Session, delete: models.Delete):
    db.add(delete)
    db.commit()
    db.refresh(delete)
    return delete

def delete_delete(db: Session, delete_id: int):
    delete = db.query(models.Delete).filter(models.Delete.id == delete_id).first()
    if delete:
        db.delete(delete)
        db.commit()
    return delete

# Dept CRUD operations
def get_depts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Dept).offset(skip).limit(limit).all()

def get_dept(db: Session, dept_code: int):
    return db.query(models.Dept).filter(models.Dept.code == dept_code).first()

def create_dept(db: Session, dept: models.Dept):
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept

def update_dept(db: Session, dept_code: int, name: str = None, office: int = None, phone: str = None, college_id: int = None):
    dept = get_dept(db, dept_code)
    if dept:
        if name:
            dept.name = name
        if office:
            dept.office = office
        if phone:
            dept.phone = phone
        if college_id:
            dept.college_id = college_id
        db.commit()
        db.refresh(dept)
    return dept

def delete_dept(db: Session, dept_code: int):
    dept = get_dept(db, dept_code)
    if dept:
        db.delete(dept)
        db.commit()
    return dept

# EducationalEmployee CRUD operations
def get_educational_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.EducationalEmployee).offset(skip).limit(limit).all()

def get_educational_employee(db: Session, edu_id: int):
    return db.query(models.EducationalEmployee).filter(models.EducationalEmployee.id == edu_id).first()

def create_educational_employee(db: Session, educational_employee: models.EducationalEmployee):
    db.add(educational_employee)
    db.commit()
    db.refresh(educational_employee)
    return educational_employee

def update_educational_employee(db: Session, edu_id: int, degree: int = None, apikey: str = None):
    educational_employee = get_educational_employee(db, edu_id)
    if educational_employee:
        if degree:
            educational_employee.degree = degree
        if apikey:
            educational_employee.apikey = apikey
        db.commit()
        db.refresh(educational_employee)
    return educational_employee

def delete_educational_employee(db: Session, edu_id: int):
    educational_employee = get_educational_employee(db, edu_id)
    if educational_employee:
        db.delete(educational_employee)
        db.commit()
    return educational_employee

# Employee CRUD operations
def get_employees(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def create_employee(db: Session, employee: models.Employee):
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee

def update_employee(db: Session, employee_id: int, first_name: str = None, last_name: str = None, position: str = None, salary: int = None, department_id: int = None):
    employee = get_employee(db, employee_id)
    if employee:
        if first_name:
            employee.first_name = first_name
        if last_name:
            employee.last_name = last_name
        if position:
            employee.position = position
        if salary:
            employee.salary = salary
        if department_id:
            employee.department_id = department_id
        db.commit()
        db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)
    if employee:
        db.delete(employee)
        db.commit()
    return employee

# Enroll CRUD operations
def get_enrolls(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Enroll).offset(skip).limit(limit).all()

def create_enroll(db: Session, enroll: models.Enroll):
    db.add(enroll)
    db.commit()
    db.refresh(enroll)
    return enroll

def delete_enroll(db: Session, enroll_id: int):
    enroll = db.query(models.Enroll).filter(models.Enroll.id == enroll_id).first()
    if enroll:
        db.delete(enroll)
        db.commit()
    return enroll

# Grade CRUD operations
def get_grades(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Grade).offset(skip).limit(limit).all()

def get_grade(db: Session, grade_id: int):
    return db.query(models.Grade).filter(models.Grade.id == grade_id).first()

def create_grade(db: Session, grade: models.Grade):
    db.add(grade)
    db.commit()
    db.refresh(grade)
    return grade

def update_grade(db: Session, grade_id: int, grade_value: int):
    grade = get_grade(db, grade_id)
    if grade:
        grade.grade = grade_value
        db.commit()
        db.refresh(grade)
    return grade

def delete_grade(db: Session, grade_id: int):
    grade = get_grade(db, grade_id)
    if grade:
        db.delete(grade)
        db.commit()
    return grade

# Professor CRUD operations
def get_professors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Professor).offset(skip).limit(limit).all()

def get_professor(db: Session, professor_id: int):
    return db.query(models.Professor).filter(models.Professor.id == professor_id).first()

def create_professor(db: Session, professor: models.Professor):
    db.add(professor)
    db.commit()
    db.refresh(professor)
    return professor

def update_professor(db: Session, professor_id: int, first_name: str = None, last_name: str = None, phone: str = None, department_id: int = None):
    professor = get_professor(db, professor_id)
    if professor:
        if first_name:
            professor.first_name = first_name
        if last_name:
            professor.last_name = last_name
        if phone:
            professor.phone = phone
        if department_id:
            professor.department_id = department_id
        db.commit()
        db.refresh(professor)
    return professor

def delete_professor(db: Session, professor_id: int):
    professor = get_professor(db, professor_id)
    if professor:
        db.delete(professor)
        db.commit()
    return professor

# Room CRUD operations
def get_rooms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Room).offset(skip).limit(limit).all()

def get_room(db: Session, room_code: int):
    return db.query(models.Room).filter(models.Room.code == room_code).first()

def create_room(db: Session, room: models.Room):
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

def update_room(db: Session, room_code: int, location: str = None, capacity: int = None):
    room = get_room(db, room_code)
    if room:
        if location:
            room.location = location
        if capacity:
            room.capacity = capacity
        db.commit()
        db.refresh(room)
    return room

def delete_room(db: Session, room_code: int):
    room = get_room(db, room_code)
    if room:
        db.delete(room)
        db.commit()
    return room

# Section CRUD operations
def get_sections(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Section).offset(skip).limit(limit).all()

def get_section(db: Session, section_id: int):
    return db.query(models.Section).filter(models.Section.id == section_id).first()

def create_section(db: Session, section: models.Section):
    db.add(section)
    db.commit()
    db.refresh(section)
    return section

def update_section(db: Session, section_id: int, year: int = None, semester: str = None, room_code: int = None, course_code: int = None, professor_id: int = None):
    section = get_section(db, section_id)
    if section:
        if year:
            section.year = year
        if semester:
            section.semester = semester
        if room_code:
            section.room_code = room_code
        if course_code:
            section.course_code = course_code
        if professor_id:
            section.professor_id = professor_id
        db.commit()
        db.refresh(section)
    return section

def delete_section(db: Session, section_id: int):
    section = get_section(db, section_id)
    if section:
        db.delete(section)
        db.commit()
    return section

# Student CRUD operations
def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def create_student(db: Session, student: models.Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def update_student(db: Session, student_id: int, first_name: str = None, last_name: str = None, phone: str = None, address: str = None, dept_code: int = None):
    student = get_student(db, student_id)
    if student:
        if first_name:
            student.first_name = first_name
        if last_name:
            student.last_name = last_name
        if phone:
            student.phone = phone
        if address:
            student.address = address
        if dept_code:
            student.dept_code = dept_code
        db.commit()
        db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = get_student(db, student_id)
    if student:
        db.delete(student)
        db.commit()
    return student

# Takes CRUD operations
def get_takes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Takes).offset(skip).limit(limit).all()

def get_take(db: Session, take_id: int):
    return db.query(models.Takes).filter(models.Takes.id == take_id).first()

def create_take(db: Session, take: models.Takes):
    db.add(take)
    db.commit()
    db.refresh(take)
    return take

def update_take(db: Session, take_id: int, student_id: int = None, course_code: int = None, year: int = None, semester: str = None):
    take = get_take(db, take_id)
    if take:
        if student_id:
            take.student_id = student_id
        if course_code:
            take.course_code = course_code
        if year:
            take.year = year
        if semester:
            take.semester = semester
        db.commit()
        db.refresh(take)
    return take

def delete_take(db: Session, take_id: int):
    take = get_take(db, take_id)
    if take:
        db.delete(take)
        db.commit()
    return take

# Get available courses for the next semester
def get_available_courses(db: Session, semester: str, year: int, skip: int = 0, limit: int = 10):
    return db.query(models.Section).filter(models.Section.semester == semester, models.Section.year == year).offset(skip).limit(limit).all()

# Register course selection for a student
def register_course_selection(db: Session, student_id: int, section_id: int):
    section = db.query(models.Section).filter(models.Section.id == section_id).first()
    if section is None:
        return None
    section.students.append(db.query(models.Student).filter(models.Student.id == student_id).first())
    db.commit()
    return section

def get_grades_by_student_and_semester(db: Session, student_id: int, semester: str, year: int):
    return db.query(models.Grade).filter(
        models.Grade.student_id == student_id,
        models.Grade.semester == semester,
        models.Grade.year == year
    ).all()
