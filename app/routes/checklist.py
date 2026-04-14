from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.db import get_db
from app.models.models import ChecklistRun
import json

router = APIRouter()

class ChecklistPayload(BaseModel):
    operator_name: str
    shift: str
    duty_moment: str
    signature_name: str
    items: list[dict]

@router.get("")
def list_checklists(db: Session = Depends(get_db)):
    rows = db.query(ChecklistRun).order_by(ChecklistRun.id.desc()).all()
    return [{"id": r.id, "operator_name": r.operator_name, "shift": r.shift, "created_at": str(r.created_at)} for r in rows]

@router.post("")
def create_checklist(payload: ChecklistPayload, db: Session = Depends(get_db)):
    row = ChecklistRun(operator_name=payload.operator_name, shift=payload.shift, duty_moment=payload.duty_moment, signature_name=payload.signature_name, summary_json=json.dumps(payload.items, ensure_ascii=False))
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"id": row.id, "message": "checklist salvo"}
