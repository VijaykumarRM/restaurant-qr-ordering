from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./restaurant.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def ensure_database_schema():
    """Ensure any new columns exist in existing tables."""
    from sqlalchemy import inspect
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    table_checks = {
        "restaurant_tables": ["points_balance"],
        "orders": ["points_used", "discount_amount", "points_earned"],
        "restaurants": ["upi_id"],
    }

    with engine.begin() as connection:
        for table_name, column_names in table_checks.items():
            if table_name not in existing_tables:
                continue  # Skip tables that don't exist yet

            existing_columns = connection.execute(text(f"PRAGMA table_info({table_name})")).fetchall()
            existing_names = {row[1] for row in existing_columns}

            for column_name in column_names:
                if column_name not in existing_names:
                    if table_name == "restaurant_tables":
                        connection.execute(
                            text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER NOT NULL DEFAULT 0")
                        )
                    elif table_name == "restaurants" and column_name == "upi_id":
                        connection.execute(
                            text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} VARCHAR(100) NULL")
                        )
                    else:
                        if column_name in {"discount_amount", "points_earned"}:
                            connection.execute(
                                text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} FLOAT NOT NULL DEFAULT 0")
                            )
                        else:
                            connection.execute(
                                text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER NOT NULL DEFAULT 0")
                            )


ensure_database_schema()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()