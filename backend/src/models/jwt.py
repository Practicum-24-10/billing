from uuid import UUID

from backend.src.models.model_mixin import OrjsonMixin


class JWTPayload(OrjsonMixin):
    is_superuser: bool
    permissions: list[str]
    user_id: UUID
