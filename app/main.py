from flask import Flask
from application.ports.http_api import init_app
from application.ports.web_dictionary import init_web_dictionary
from application.ports.demo_rhymes import init_rhyme_demo
from infrastructure.database import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    init_db(app)  # Initialize the database here
    init_app(app)  # Initialize other parts of the application
    init_web_dictionary(app)
    init_rhyme_demo(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
