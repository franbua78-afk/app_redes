from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..deps import get_current_user
from ..db.session import get_db
from ..db.models import Template


router = APIRouter(prefix="/templates", tags=["templates"])


class TemplateRequest(BaseModel):
    name: str
    params: dict


@router.post("")
def create_template(payload: TemplateRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    t = Template(user_id=user.id, name=payload.name, params=payload.params)
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"id": t.id}


@router.get("")
def list_templates(user=Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(Template).filter(Template.user_id == user.id).order_by(Template.created_at.desc()).all()
    return [{"id": t.id, "name": t.name, "params": t.params} for t in items]

