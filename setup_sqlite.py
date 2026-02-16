from app.main import create_app
from infrastructure.database import db
# Ensure models are imported so SQLAlchemy knows about them
from infrastructure.repository.models import BookDTO

def setup():
    app = create_app()
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created.")

if __name__ == "__main__":
    setup()
