import uuid
from db.redis import redis_client

SESSION_TTL = 60 * 60 * 24  # 1 day

""" async def create_session(user_id: str) -> str:
    session_id = str(uuid.uuid4())
    await redis_client.setex(
        f"session:{session_id}",
        SESSION_TTL,
        user_id
    )
    return session_id """

async def delete_session(session_id: str):
    await redis_client.delete(f"session:{session_id}")


async def get_user_id(session_id: str) -> str | None:
    return await redis_client.get(f"session:{session_id}")