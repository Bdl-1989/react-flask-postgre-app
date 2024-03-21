from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import User
from schemas import UserSchema
user_bp = Blueprint('users', __name__)


@user_bp.route('/all', methods=['GET'])
@jwt_required()
def get_users():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 3, type=int)

    users = User.query.paginate(
        page=page, per_page=per_page, error_out=False
    )

    result = UserSchema(many=True).dump(users)

    return jsonify({
        'users': result,
        'page': users.page,
        'per_page': users.per_page,
        'total_pages': users.pages,
        'total_users': users.total
    }), 200