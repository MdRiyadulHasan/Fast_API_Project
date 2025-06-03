from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class VendorOut(BaseModel):
    id: int
    textId: Optional[str]
    name: Optional[str] = Field(None, alias='title')  # 'title' from model will appear as 'name' in API
    details: Optional[str]
    memberEmail: Optional[str]
    url: Optional[str]
    status: Optional[str]
    created: datetime
    updated: Optional[datetime]

    model_config = {
        "from_attributes": True  # Enables ORM compatibility in Pydantic v2
    }
    
class VendorListResponse(BaseModel):
    total: int
    items: list[VendorOut]


class VendorCreate(BaseModel):
    textId: Optional[str]
    title: Optional[str]
    details: Optional[str]
    memberEmail: Optional[str]
    url: Optional[str]
    status: Optional[str] = 'Y'

    class Config:
        from_attributes = True  # for SQLAlchemy compatibility in Pydantic v2

class VendorUpdate(BaseModel):
    textId: Optional[str]
    title: Optional[str]
    details: Optional[str]
    memberEmail: Optional[str]
    url: Optional[str]
    status: Optional[str]