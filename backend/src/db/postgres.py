from backend.src.db.storage import PostgresStorage

pg: PostgresStorage | None = None


async def get_postgres() -> PostgresStorage | None:
    return pg
