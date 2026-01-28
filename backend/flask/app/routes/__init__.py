from flask import Blueprint

from app.routes import prediction_routes

def register_blueprints(app):
    app.register_blueprint(prediction_routes.prediction_bp)
