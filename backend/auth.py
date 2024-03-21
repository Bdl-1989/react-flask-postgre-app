from flask import Blueprint, request, jsonify, make_response
from models import User, TokenBlockList
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt,current_user,get_jwt_identity

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401
    # Create the tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    
    # Create the response
    response = make_response({
        "message": "User logged in",
        "token": {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    },201)

    # Set the tokens as cookies
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', refresh_token, httponly=True)

    return response

@auth.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    user = User.get_user_by_username(username=data.get('username'))
    if user:
        return jsonify({'error': 'User already exists'}), 409
    
    new_user = User(username=data.get('username'), email=data.get('email'))
    new_user.set_password(data.get('password')) 
    new_user.save()

    return jsonify({'message': 'User created'}),201

@auth.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt['type']
    token = TokenBlockList(jti=jti)
    token.save()

    return jsonify({'message': f'User logged out. Token {token_type} has been revoked'}), 200

@auth.route('/whoami', methods=['GET'])
@jwt_required()
def whoami():
    claims = get_jwt()
    return jsonify(
        {'message': 'You are logged in',
         'claims': claims,
         'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
         }
         }
    )

@auth.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refress_access():
    indentity = get_jwt_identity()

    return jsonify({
        'indentity': indentity,
        'access_token': create_access_token(identity=indentity)
    }), 200