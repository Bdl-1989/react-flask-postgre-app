from flask import Flask, jsonify
from auth import auth
from users import user_bp
from extension import db
from extension import jwt
from models import User, TokenBlockList
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/users'
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    
    with app.app_context():
        db.create_all()

    # Registering blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')

    # # jwt error handling
    # @jwt.expired_token_loader
    # def expired_token_callback(jwt_header, jwt_data):
    #     return jsonify({'error': 'Token has expired'}), 401

    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     return jsonify({'error': 'Signature verification failed'}), 401


    # @jwt.unauthorized_loader
    # def unauthorized_callback(error):
    #     return jsonify({'error': 'Unauthorized'}), 401


    # additional claims
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        return {'role': 'admin' if identity == '1' else 'user'}


    # load user


    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = TokenBlockList.query.filter_by(jti=jti).first()
        return token is not None

    return app
    
 