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

7. Запуск тестов
```bash
pytest tests/test_auditor.py -v
```

8. Проверка Quality Agent
```bash
python3 - <<EOF
from app.agents.quality import QualityAgent
from app.models.schemas import AdInput

agent = QualityAgent()
ad = AdInput(
    title="Продам велосипед",
    description="Почти новый, отличное состояние, алюминиевая рама",
    category="sport"
)

score, issues = agent.analyze(ad)
print(score, issues)
EOF
```