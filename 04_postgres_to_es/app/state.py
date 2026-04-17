from app.storage import BaseStorage


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.data = storage.retrieve()

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value):
        self.data[key] = value
        self.storage.save(self.data)
