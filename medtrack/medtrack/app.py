from flask import Flask
import os

from .extensions import db, login_manager


def create_app() -> Flask:
	app = Flask(__name__, instance_relative_config=True)

	app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")

	os.makedirs(app.instance_path, exist_ok=True)
	database_path = os.path.join(app.instance_path, "medtrack.sqlite3")
	app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	db.init_app(app)
	login_manager.init_app(app)

	from .auth import auth_bp, ensure_default_admin
	from .inventory import inventory_bp

	app.register_blueprint(auth_bp)
	app.register_blueprint(inventory_bp)

	@app.cli.command("db-upgrade")
	def db_upgrade() -> None:
		from . import models  # noqa: F401
		db.create_all()
		ensure_default_admin()

	@app.shell_context_processor
	def shell_context():
		from .models import User, Medicine, Transaction
		return {
			"db": db,
			"User": User,
			"Medicine": Medicine,
			"Transaction": Transaction,
		}

	with app.app_context():
		from . import models  # noqa: F401
		db.create_all()
		ensure_default_admin()

	return app


app = create_app()