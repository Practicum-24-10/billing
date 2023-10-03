from backend.src.kassa.kassa import YooKassa

yk: YooKassa | None = None


async def get_yookassa() -> YooKassa | None:
    return yk
