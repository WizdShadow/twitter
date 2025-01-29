from sqlalchemy.future import select
from database import Medias

async def get_id(id, session):
    query = select(Medias).where(Medias.id.in_(id))
    result = await session.execute(query)
    attachments = result.scalars().all()
    return attachments