from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.config import settings
from app.models.models import Person

router = APIRouter()

@router.get("")
def list_people(db: Session = Depends(get_db)):
    rows = db.query(Person).order_by(Person.name.asc()).all()
    return [{"id": r.id, "name": r.name, "kind": r.kind, "doc_photo_path": r.doc_photo_path, "face_photo_path": r.face_photo_path} for r in rows]

@router.post("")
def create_person(kind: str = Form(...), name: str = Form(...), cargo: str = Form(""), doc_id: str = Form(""), phone: str = Form(""), cnh_photo: UploadFile | None = File(default=None), face_photo: UploadFile | None = File(default=None), db: Session = Depends(get_db)):
    doc_path = None
    face_path = None
    if cnh_photo:
        doc_target = settings.fotos_dir / f"cnh_{cnh_photo.filename}"
        doc_target.write_bytes(cnh_photo.file.read())
        doc_path = str(doc_target)
    if face_photo:
        face_target = settings.fotos_dir / f"face_{face_photo.filename}"
        face_target.write_bytes(face_photo.file.read())
        face_path = str(face_target)
    row = Person(kind=kind, name=name, cargo=cargo, doc_id=doc_id, phone=phone, doc_photo_path=doc_path, face_photo_path=face_path)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "name": row.name}
