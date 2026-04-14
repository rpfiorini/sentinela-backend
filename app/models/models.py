from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.db import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    cnpj = Column(String(32))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="ADMIN")
    active = Column(Integer, nullable=False, default=1)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    kind = Column(String(40), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    name = Column(String(200), nullable=False)
    cargo = Column(String(120))
    doc_id = Column(String(60))
    phone = Column(String(40))
    status = Column(String(20), default="ATIVO")
    face_photo_path = Column(Text)
    doc_photo_path = Column(Text)
    notes = Column(Text)
    employee_code = Column(String(60))
    admission_date = Column(String(30))
    shift = Column(String(60))
    access_start = Column(String(10))
    access_end = Column(String(10))
    access_days = Column(String(60))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Correspondence(Base):
    __tablename__ = "correspondences"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=True)
    sender = Column(String(200))
    ctype = Column(String(60))
    tracking_code = Column(String(120))
    courier_name = Column(String(120))
    courier_doc = Column(String(60))
    receiver_signature_path = Column(Text)
    package_photo_path = Column(Text)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    operator_username = Column(String(80), nullable=False)

class ChecklistRun(Base):
    __tablename__ = "checklist_runs"
    id = Column(Integer, primary_key=True)
    operator_name = Column(String(120), nullable=False)
    shift = Column(String(60), nullable=False)
    duty_moment = Column(String(60), nullable=False)
    signature_name = Column(String(120), nullable=False)
    summary_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
