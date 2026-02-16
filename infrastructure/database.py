from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

def init_db(app):
    # MySQL Configuration
    # Using root with empty password as verified by setup script
    import os
    db_uri = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost:3306/library_db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    
    # SQLite Configuration (Commented out)
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # # Go up one level from infrastructure to root
    # db_path = os.path.join(basedir, '..', 'library.db')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
