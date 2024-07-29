from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from .base import Base

# Association tables for many-to-many relationships
student_section_association = Table(
    'student_section',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('student.SId', ondelete='CASCADE'), primary_key=True),
    Column('section_id', Integer, ForeignKey('section.SecId', ondelete='CASCADE'), primary_key=True)
)

college_dept_association = Table(
    'college_dept',
    Base.metadata,
    Column('college_id', Integer, ForeignKey('college.CID', ondelete='CASCADE'), primary_key=True),
    Column('dept_code', Integer, ForeignKey('dept.DCode', ondelete='CASCADE'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(255))  # Can be 'student', 'professor', 'admin'

class Book(Base):
    __tablename__ = 'book'
    id = Column('BId', Integer, primary_key=True, index=True)
    title = Column('BTitle', String(255), index=True)
    author = Column('BAuthor', String(255))
    pub_date = Column('BPubDate', Date)
    l_code = Column('LCode', Integer)

    borrows = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")

class Borrow(Base):
    __tablename__ = 'borrow'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column('book_BId', Integer, ForeignKey('book.BId', ondelete='CASCADE'))
    student_id = Column('student_SId', Integer, ForeignKey('student.SId', ondelete='CASCADE'))
    date_of_borrow = Column('dateOFBorrow', Date)
    return_time = Column('returnTime', Date)

    book = relationship("Book", back_populates="borrows")
    student = relationship("Student", back_populates="borrows")

class College(Base):
    __tablename__ = 'college'
    id = Column('CID', Integer, primary_key=True, index=True)
    name = Column('CName', String(255))
    office = Column('COffice', Integer)
    phone = Column('CPhone', String(255))
    dean = Column('CDean', Integer)
    apikey = Column('apikey', String(255), nullable=False)

    depts = relationship('Dept', secondary=college_dept_association, back_populates='colleges')

class Course(Base):
    __tablename__ = 'course'
    code = Column('CCode', Integer, primary_key=True, index=True)
    name = Column('CoName', String(255))
    level = Column('Level', String(255))
    description = Column('CDesc', String(255))
    dept_code = Column('DCode', Integer, ForeignKey('dept.DCode'))
    credit = Column('Credit', Integer)

    sections = relationship('Section', back_populates='course', cascade="all, delete-orphan")
    takes = relationship('Takes', back_populates='course', cascade="all, delete-orphan")

class Delete(Base):
    __tablename__ = 'delete'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column('SId', Integer, ForeignKey('student.SId', ondelete='CASCADE'))
    section_id = Column('SecId', Integer, ForeignKey('section.SecId', ondelete='CASCADE'))
    type = Column('Type', Integer)
    date_of_deletion = Column('DOD', Date)

class Dept(Base):
    __tablename__ = 'dept'
    code = Column('DCode', Integer, primary_key=True, index=True)
    name = Column('DName', String(255))
    office = Column('DOffice', Integer)
    phone = Column('DPhone', String(255))
    college_id = Column('CID', Integer, ForeignKey('college.CID'))

    colleges = relationship('College', secondary=college_dept_association, back_populates='depts')
    professors = relationship('Professor', back_populates='department')
    employees = relationship('Employee', back_populates='department')
    students = relationship('Student', back_populates='department')

class EducationalEmployee(Base):
    __tablename__ = 'educational_employee'
    id = Column('EId', Integer, primary_key=True, index=True)
    degree = Column(Integer)
    edu_id = Column('eduID', Integer)
    apikey = Column('apikey', String(255), nullable=False)

class Employee(Base):
    __tablename__ = 'employee'
    id = Column('EId', Integer, primary_key=True, index=True)
    first_name = Column('Fname', String(255))
    last_name = Column('Lname', String(255))
    position = Column('position', String(255))
    salary = Column('salary', Integer)
    department_id = Column('DCode', Integer, ForeignKey('dept.DCode'))

    department = relationship('Dept', back_populates='employees')

class Grade(Base):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column('SId', Integer, ForeignKey('student.SId', ondelete='CASCADE'))
    section_id = Column('SecId', Integer, ForeignKey('section.SecId', ondelete='CASCADE'))
    grade = Column('grade', Integer)

class Professor(Base):
    __tablename__ = 'professor'
    id = Column('PId', Integer, primary_key=True, index=True)
    first_name = Column('Fname', String(255))
    last_name = Column('Lname', String(255))
    phone = Column('Phone', String(255))
    department_id = Column('DCode', Integer, ForeignKey('dept.DCode'))

    sections = relationship('Section', back_populates='professor', cascade="all, delete-orphan")
    department = relationship('Dept', back_populates='professors')

class Room(Base):
    __tablename__ = 'room'
    code = Column('RCode', Integer, primary_key=True, index=True)
    location = Column('RLocation', String(255))
    capacity = Column('Capacity', Integer)

    sections = relationship('Section', back_populates='room', cascade="all, delete-orphan")

class Section(Base):
    __tablename__ = 'section'
    id = Column('SecId', Integer, primary_key=True, index=True)
    year = Column('Year', Integer)
    semester = Column('Semester', String(255))
    room_code = Column('RCode', Integer, ForeignKey('room.RCode'))
    course_code = Column('CCode', Integer, ForeignKey('course.CCode'))
    professor_id = Column('PId', Integer, ForeignKey('professor.PId'))

    students = relationship('Student', secondary=student_section_association, back_populates='sections')
    room = relationship('Room', back_populates='sections')
    course = relationship('Course', back_populates='sections')
    professor = relationship('Professor', back_populates='sections')

class Student(Base):
    __tablename__ = 'student'
    id = Column('SId', Integer, primary_key=True, index=True)
    first_name = Column('Fname', String(255))
    last_name = Column('Lname', String(255))
    phone = Column('Phone', String(255))
    address = Column('Address', String(255))
    dept_code = Column('DCode', Integer, ForeignKey('dept.DCode'))

    borrows = relationship("Borrow", back_populates="student", cascade="all, delete-orphan")
    sections = relationship('Section', secondary=student_section_association, back_populates='students')
    takes = relationship('Takes', back_populates='student', cascade="all, delete-orphan")
    department = relationship('Dept', back_populates='students')

class Takes(Base):
    __tablename__ = 'takes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column('SId', Integer, ForeignKey('student.SId', ondelete='CASCADE'))
    course_code = Column('CCode', Integer, ForeignKey('course.CCode', ondelete='CASCADE'))
    year = Column('Year', Integer)
    semester = Column('Semester', String(255))

    student = relationship('Student', back_populates='takes')
    course = relationship('Course', back_populates='takes')
