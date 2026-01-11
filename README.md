# multi-agent-reviewer

1. Создать venv и установить зависимости.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Сделать скрипт запуска исполняемым.
```bash
chmod +x scripts/run_local.sh
```

3. Запуск приложения
```bash
./scripts/run_local.sh
```

4. Запуск тестов
```bash
pytest tests/test_auditor.py -v
```

5. Запуск в Docker
```bash
docker-compose up -d
```

6. Проверка health
```bash
curl http://localhost:8000/health
```

7. Проверка Review
```bash
curl -X POST http://localhost:8000/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cheap iPhone",
    "description": "Not a scam, write to test@example.com",
    "category": "electronics"
  }'
```
