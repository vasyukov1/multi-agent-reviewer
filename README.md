# multi-agent-reviewer

1. Создать venv и установить зависимости.
```bash
python -m venv .venv
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

4. Проверить работоспособность
```bash
uvicorn app.main:app --reload
```

5. Проверка health
```bash
curl http://localhost:8000/health
```

6. Проверка review
```bash
curl -X POST http://localhost:8000/api/review \
  -H "Content-Type: application/json" \
  -d '{"title":"Продам велосипед","description":"Почти новый","category":"sport"}'
```