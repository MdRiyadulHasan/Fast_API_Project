from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional

from app.vendor.schemas import VendorOut, VendorListResponse, VendorCreate
from app.vendor.services import get_all_vendors, create_vendor

router = APIRouter()


@router.get(
    "/vendors/",
    response_model=VendorListResponse,
    summary="List all vendors with filters and pagination"
)
async def vendor_list(
    status: Optional[str] = Query(None, description="Filter by status"),
    member_email: Optional[str] = Query(None, description="Filter by member email"),
    title: Optional[str] = Query(None, description="Filter by vendor title"),
    limit: int = Query(10, ge=1, le=100, description="Number of vendors to return"),
    offset: int = Query(0, ge=0, description="Number of vendors to skip"),
):
    total, vendors = await get_all_vendors(status, member_email, title, limit, offset)
    return {"total": total, "items": vendors}


@router.post(
    "/vendors-creation/",
    response_model=VendorOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new vendor"
)
async def create_new_vendor(vendor_in: VendorCreate):
    vendor = await create_vendor(vendor_in)
    if not vendor:
        raise HTTPException(status_code=400, detail="Failed to create vendor")
    return vendor
