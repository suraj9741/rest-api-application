from sqlalchemy import Column, Integer, String, Date
from app.db import Base

class Student(Base):
    __tablename__ = "student"   # 👈 table name changed

    student_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    date_of_birth = Column(Date)
    gender = Column(String(10))


