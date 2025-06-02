from sqlalchemy.future import select
from sqlalchemy import and_, func
from app.db.session import AsyncSessionLocal
from datetime import datetime
from app.vendor.models import Vendor
from typing import Optional, List, Tuple
from app.vendor.schemas import VendorCreate

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
