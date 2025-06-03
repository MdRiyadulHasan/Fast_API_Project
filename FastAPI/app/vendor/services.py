from sqlalchemy.future import select
from sqlalchemy import and_, func
from app.db.session import AsyncSessionLocal
# from app.db import async_session
from datetime import datetime
from app.vendor.models import Vendor
from typing import Optional, List, Tuple
from app.vendor.schemas import VendorCreate, VendorUpdate

async def get_all_vendors(
    status: Optional[str] = None,
    member_email: Optional[str] = None,
    title: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> Tuple[int, List[Vendor]]:
    async with AsyncSessionLocal() as session:
        filters = []

        if status:
            filters.append(Vendor.status == status)
        if member_email:
            filters.append(Vendor.memberEmail.ilike(f"%{member_email}%"))
        if title:
            filters.append(Vendor.title.ilike(f"%{title}%"))

        stmt = select(Vendor).where(and_(*filters)).limit(limit).offset(offset)
        count_stmt = select(func.count()).select_from(Vendor).where(and_(*filters))

        result = await session.execute(stmt)
        vendors = result.scalars().all()

        total_result = await session.execute(count_stmt)
        total = total_result.scalar()

        return total, vendors


async def create_vendor(vendor_in: VendorCreate):
    async with AsyncSessionLocal() as session:
        new_vendor = Vendor(
            textId=vendor_in.textId,
            title=vendor_in.title,
            details=vendor_in.details,
            memberEmail=vendor_in.memberEmail,
            url=vendor_in.url,
            status=vendor_in.status,
            created=datetime.utcnow()
        )
        session.add(new_vendor)
        await session.commit()
        await session.refresh(new_vendor)  # to get the generated ID and timestamps
        return new_vendor

  
async def delete_vendor_by_id(vendor_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Vendor).where(Vendor.id == vendor_id))
        vendor = result.scalar_one_or_none()
        if not vendor:
            return False
        await session.delete(vendor)
        await session.commit()
        return True

async def update_vendor(vendor_id: int, vendor_in: VendorUpdate):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Vendor).where(Vendor.id == vendor_id))
        vendor = result.scalar_one_or_none()

        if not vendor:
            return None  # Or raise exception

        # Update fields
        vendor.textId = vendor_in.textId or vendor.textId
        vendor.title = vendor_in.title or vendor.title
        vendor.details = vendor_in.details or vendor.details
        vendor.memberEmail = vendor_in.memberEmail or vendor.memberEmail
        vendor.url = vendor_in.url or vendor.url
        vendor.status = vendor_in.status or vendor.status
        vendor.updated = datetime.utcnow()

        await session.commit()
        await session.refresh(vendor)

        return vendor

