from flask_migrate import Migrate

from backend import create_app, db

app = create_app()
migrate = Migrate(app, db)
migrate.init_app(app)
