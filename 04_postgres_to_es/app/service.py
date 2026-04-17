import random
import time
from datetime import datetime, timezone


def _default_cursor():
    return {
        "ts": "1970-01-01T00:00:00+00:00",
        "id": "00000000-0000-0000-0000-000000000000",
    }


def _advance_cursor(batch: list[dict], current: dict) -> dict:
    if not batch:
        return current
    last = batch[-1]
    return {"ts": last["modified"].isoformat(), "id": str(last["id"])}


class ETLService:
    def __init__(self, settings, state, extractor, transformer, loader):
        self.settings = settings
        self.state = state
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run_once(self):
        fw_cursor = self.state.get("fw_cursor", _default_cursor())
        person_cursor = self.state.get("person_cursor", _default_cursor())
        genre_cursor = self.state.get("genre_cursor", _default_cursor())

        fw_batch = self.extractor.fetch_film_work_batch(
            fw_cursor["ts"], fw_cursor["id"], self.settings.batch_size
        )
        person_batch = self.extractor.fetch_person_batch(
            person_cursor["ts"], person_cursor["id"], self.settings.batch_size
        )
        genre_batch = self.extractor.fetch_genre_batch(
            genre_cursor["ts"], genre_cursor["id"], self.settings.batch_size
        )

        changed_film_ids = {str(i["id"]) for i in fw_batch}
        changed_film_ids.update(
            self.extractor.film_ids_by_person_ids([str(i["id"]) for i in person_batch])
        )
        changed_film_ids.update(
            self.extractor.film_ids_by_genre_ids([str(i["id"]) for i in genre_batch])
        )

        if changed_film_ids:
            payload = self.extractor.fetch_movies_payload(list(changed_film_ids))
            docs = self.transformer.transform(payload)
            self.loader.bulk_upsert(docs)

        self.state.set("fw_cursor", _advance_cursor(fw_batch, fw_cursor))
        self.state.set("person_cursor", _advance_cursor(person_batch, person_cursor))
        self.state.set("genre_cursor", _advance_cursor(genre_batch, genre_cursor))
        self.state.set("last_run_at", datetime.now(timezone.utc).isoformat())

    def run_forever(self):
        delay = self.settings.backoff_initial_sec
        while True:
            try:
                self.loader.ensure_index()
                self.run_once()
                delay = self.settings.backoff_initial_sec
                time.sleep(self.settings.poll_interval_sec)
            except Exception:
                sleep_for = min(delay, self.settings.backoff_max_sec) + random.uniform(
                    0, self.settings.backoff_jitter_sec
                )
                time.sleep(sleep_for)
                delay = min(delay * 2, self.settings.backoff_max_sec)
