def get_sqlite_env() -> str:
    return """
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
"""


def get_postgress_env() -> str:
    return """POSTGRES_USER=admin
POSTGRES_PASSWORD=safepassword
POSTGRES_DB=database
PGADMIN_MAIL=admin@email.com
PGADMIN_PW=adminpassword
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db?check_same_thread=false"
"""
