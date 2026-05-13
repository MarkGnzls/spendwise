from flask import Flask

def create_app():
    app = Flask(__name__)

    # register routes here (if using blueprints)
    # from .routes import main
    # app.register_blueprint(main)

    return app