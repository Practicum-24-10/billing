from backend.src.auth.abc_key import AbstractKey

pk: AbstractKey | None = None


async def get_pk() -> AbstractKey | None:
    return pk
