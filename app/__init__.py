from flask import Flask
from app.config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes.dashboard import dashboard_bp
    from app.routes.deals import deals_bp
    from app.routes.ic import ic_bp
    from app.routes.data_room import data_room_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(deals_bp, url_prefix='/deals')
    app.register_blueprint(ic_bp, url_prefix='/ic')
    app.register_blueprint(data_room_bp, url_prefix='/vdr')

    # Create tables and auto-seed if empty
    with app.app_context():
        db.create_all()
        from app.seed import auto_seed
        auto_seed()

    return app