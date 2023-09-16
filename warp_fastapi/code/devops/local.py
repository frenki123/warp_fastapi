def get_startup_script() -> str:
    return """#!/bin/bash
echo "Creating virtual enviroment .venv"
python -m venv .venv
source ./.venv/Scripts/activate
echo "Instaling requirements"
pip install -r requirements.txt
echo "Lint and formating check"
echo "Database initial migration"
alembic revision -m "Tables creation" --autogenerate
alembic upgrade head
echo "mypy check"
mypy .
echo "tests"
pytest --cov
echo "starting app"
uvicorn app.main:app --reload"""
