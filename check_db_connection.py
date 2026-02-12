from app.main import create_app
from infrastructure.database import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Try to connect and execute a simple query
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Successfully connected to the database!")
            print(f"Test query result: {result.scalar()}")
    except Exception as e:
        print(f"Failed to connect to the database.")
        print(f"Error: {e}")
