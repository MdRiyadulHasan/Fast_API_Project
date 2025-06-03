from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional

from app.vendor.schemas import VendorOut, VendorListResponse, VendorCreate, VendorUpdate
from app.vendor.services import get_all_vendors, create_vendor, delete_vendor_by_id, update_vendor

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




@router.delete(
    "/delete_vendors/{vendor_id}/",
    status_code=status.HTTP_200_OK,
    summary="Delete a vendor by ID"
)
async def delete_vendor(vendor_id: int):
    deleted = await delete_vendor_by_id(vendor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vendor not found or already deleted")
    return {"message": f"Vendor with ID {vendor_id} has been deleted"}


@router.put("/vendor_update/{vendor_id}/", response_model=VendorOut)
async def update_existing_vendor(vendor_id: int, vendor_in: VendorUpdate):
    updated_vendor = await update_vendor(vendor_id, vendor_in)
    if not updated_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return updated_vendor