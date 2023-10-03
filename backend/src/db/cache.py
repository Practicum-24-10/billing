from abc import ABC, abstractmethod

from aioredis import Redis


class AbstractCache(ABC):
    @abstractmethod
    async def get(self, _id: bytes):
        pass

    @abstractmethod
    async def set(self, _id: bytes, data: bytes):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def delete(self, _id: bytes):
        pass


class RedisCache(AbstractCache):
    def __init__(self, host: str, port: int, expire: int):
        self._connect = Redis(host=host, port=port)
        self._expire = expire

    async def get(self, _id: bytes):
        return await self._connect.get(name=_id)

    async def set(self, _id: bytes, data: bytes):
        return await self._connect.set(name=_id, value=data, ex=self._expire)

    async def close(self):
        await self._connect.close()

    async def delete(self, _id: bytes):
        return await self._connect.delete(_id)
