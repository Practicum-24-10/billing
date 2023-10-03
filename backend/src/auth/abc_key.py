from abc import ABC, abstractmethod


class AbstractKey(ABC):
    key: str
    algorithms: list[str]
    pl_is_superuser: str
    pl_permissions: str
    pl_sub: str

    @abstractmethod
    async def _load(self, path: str):
        pass


class RsaKey(AbstractKey):
    key: str
    algorithms: list[str]
    pl_is_superuser: str
    pl_permissions: str
    pl_sub: str

    def __init__(self, path: str, algorithms: list[str]):
        self._load(path)
        self.algorithms = algorithms
        self.pl_permissions = "permissions"
        self.pl_is_superuser = "is_superuser"
        self.pl_sub = "sub"

    def _load(self, path: str):
        self.key = open(path).read()
