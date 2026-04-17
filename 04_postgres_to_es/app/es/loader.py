from elasticsearch import Elasticsearch, helpers

from app.es.schema import MOVIES_INDEX_SCHEMA


class ElasticsearchLoader:
    def __init__(self, host: str, index: str):
        self.client = Elasticsearch(hosts=[host])
        self.index = index

    def ensure_index(self) -> None:
        if not self.client.indices.exists(index=self.index):
            self.client.indices.create(index=self.index, body=MOVIES_INDEX_SCHEMA)

    def bulk_upsert(self, docs: list[dict]) -> None:
        if not docs:
            return
        actions = [
            {
                "_op_type": "index",
                "_index": self.index,
                "_id": doc["id"],
                "_source": doc,
            }
            for doc in docs
        ]
        helpers.bulk(self.client, actions, raise_on_error=True)
