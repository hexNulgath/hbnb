from datetime import timedelta
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set up the API
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as login_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')  # Fixed typo
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(login_ns, path='/api/v1')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    return app
