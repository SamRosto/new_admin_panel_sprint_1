import json
import os
import tempfile
from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def save(self, state: dict) -> None: ...

    @abstractmethod
    def retrieve(self) -> dict: ...


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)

    def save(self, state: dict) -> None:
        parent = os.path.dirname(self.file_path) or "."
        with tempfile.NamedTemporaryFile(
            "w", dir=parent, delete=False, encoding="utf-8"
        ) as tmp:
            json.dump(state, tmp, ensure_ascii=False)
            tmp.flush()
            os.fsync(tmp.fileno())
            tmp_name = tmp.name
        os.replace(tmp_name, self.file_path)

    def retrieve(self) -> dict:
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)
