from ...config import NameConfig


def get_dockerfile(config: NameConfig) -> str:
    return """FROM python:3

WORKDIR /app
RUN mkdir app

COPY alembic.ini ./
COPY requirements.txt ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./app ./app


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
"""


def get_compose_file() -> str:
    return """version: '3.1'

services:

  postgres:
    container_name: postgres
    image: postgres:latest
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    ports:
      - "5432:5432"
    restart: always
    networks:
      - app-network
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_MAIL}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PW}
    ports:
      - "5050:80"
    restart: always
    networks:
      - app-network

  web:
    build:
      context: .
      dockerfile: dockerfile
    ports:
      - "8000:80"
    environment:
      - SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      - PYTHONUNBUFFERED=1
    networks:
      - app-network
    depends_on:
      - postgres
    volumes:
      - ./app:/app/app
      - ./tests:/app/tests

volumes:
  postgres_data:

networks:
  app-network:
"""


def get_dockerignore() -> str:
    return """# Git
.git
.gitignore

# Docker
docker-compose.yml
Dockerfile
.docker
.dockerignore

# Byte-compiled / optimized / DLL files
**/__pycache__/
**/*.py[cod]

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
.env

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.cache
nosetests.xml
coverage.xml

# VS Code
.vscode/
"""


def get_compose_file_persistent_data() -> str:
    return """version: '3.1'

services:

  postgres:
    container_name: postgres
    image: postgres:latest
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    ports:
      - "5432:5432"
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
      - app-network

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_MAIL}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_PW}
    ports:
      - "5050:80"
    restart: always
    networks:
      - app-network

  web:
    build:
      context: .
      dockerfile: dockerfile
    ports:
      - "8000:80"
    environment:
      - SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
    networks:
      - app-network
    volumes:
      - type: volume
        source: mydata
        target: /data
        volume:
          nocopy: true
      - type: bind
        source: ./
        target: /app/
    depends_on:
      - postgres

volumes:
  postgres_data:
  mydata:

networks:
  app-network:
"""
