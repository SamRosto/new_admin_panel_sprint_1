# Гайд как запустить приложение

### Запустить docker compose
```
docker compose up -d --build
```

### Создать схему для Postgres
```
docker compose exec db psql -U app -d movies_database -c "CREATE SCHEMA content AUTHORIZATION app;"
```

### Проверить что схема `content` создалась
```
docker compose exec db psql -U app -d movies_database -c "\dt"
docker compose exec db psql -U app -d movies_database -c "\dt content.*"
```

### Применить миграции
```
docker compose exec web python manage.py migrate
```

### Применить загрузку данных из SQLite в Postgres
```
docker compose --profile import run --rm sqlite_to_postgres
```

### Запустить/перезапустить ES + ETL если потребуется
```
docker compose up -d elasticsearch etl
docker compose restart etl
```

### Проверить, что индекс movies создан и наполняется
```
docker compose exec elasticsearch curl -s http://127.0.0.1:9200/_cat/indices?v
docker compose exec elasticsearch curl -s http://127.0.0.1:9200/movies/_count
```

### Админка будет доступеа по адресу `http://localhost:8000/admin/`

### API будет доступно по адресу `http://localhost:8000/api/v1/movies/`