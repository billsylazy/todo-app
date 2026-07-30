from flask import Flask

from todoapp import db as db_module
from todoapp.config import Config
from todoapp.tasks.routes import bp as tasks_bp


def create_app(config_class=Config, **config_overrides):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config.update(config_overrides)

    db_module.init_app(app)

    with app.app_context():
        db_module.run_migrations()

    app.register_blueprint(tasks_bp)

    return app
