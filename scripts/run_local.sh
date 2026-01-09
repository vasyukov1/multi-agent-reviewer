#!/bin/bash

# Скрипт для запуска FastAPI

set -e

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Запуск приложения"
echo "Сервер будет доступен по адресам:"
echo "- http://localhost:8000"
echo "- http://0.0.0.0:8000"
echo "Документация: http://localhost:8000/docs"
echo ""
echo "Для остановки нажмите Ctrl+C"

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
