from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.config import settings
from app.models.models import Correspondence
from datetime import datetime

router = APIRouter()

@router.get("")
def list_correspondences(db: Session = Depends(get_db)):
    rows = db.query(Correspondence).order_by(Correspondence.id.desc()).all()
    return [{"id": r.id, "tracking_code": r.tracking_code, "sender": r.sender, "operator_username": r.operator_username, "signature": r.receiver_signature_path} for r in rows]

@router.post("")
def create_correspondence(sender: str = Form(""), ctype: str = Form(""), tracking_code: str = Form(""), courier_name: str = Form(""), courier_doc: str = Form(""), operator_username: str = Form(...), signature: UploadFile | None = File(default=None), package_photo: UploadFile | None = File(default=None), db: Session = Depends(get_db)):
    sign_path = None
    pkg_path = None
    if signature:
        target = settings.assinaturas_dir / f"sign_{signature.filename}"
        target.write_bytes(signature.file.read())
        sign_path = str(target)
    if package_photo:
        target = settings.fotos_dir / f"pkg_{package_photo.filename}"
        target.write_bytes(package_photo.file.read())
        pkg_path = str(target)
    row = Correspondence(sender=sender, ctype=ctype, tracking_code=tracking_code, courier_name=courier_name, courier_doc=courier_doc, operator_username=operator_username, receiver_signature_path=sign_path, package_photo_path=pkg_path)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "tracking_code": row.tracking_code, "received_at": datetime.utcnow().isoformat()}
