from app.db.session import engine
from app.db.base import Base

# Import all models so Base.metadata includes them
from app.users.models import Vendor  # this ensures Vendor is registered

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)