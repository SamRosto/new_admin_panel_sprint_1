import logging

from app.settings import settings

from app.es.extractor import PostgresExtractor
from app.transformer import MoviesTransformer
from app.es.loader import ElasticsearchLoader
from app.storage import JsonFileStorage
from app.service import ETLService
from app.state import State


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("ETL service starting")

    storage = JsonFileStorage(settings.state_file)
    state = State(storage)

    with PostgresExtractor(settings.pg_dsn) as extractor:
        transformer = MoviesTransformer()
        loader = ElasticsearchLoader(settings.es_host, settings.es_index)

        ETLService(settings, state, extractor, transformer, loader).run_forever()


if __name__ == "__main__":
    main()
