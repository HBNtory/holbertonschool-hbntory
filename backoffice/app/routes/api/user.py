from flask import Blueprint, request

from app.exceptions.user_exceptions import EmailAlreadyExists, UserNotFound
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import UserService

bp = Blueprint("user_api", __name__, url_prefix="/api/users")


@bp.route("", methods=["POST"])
def create_user():
    service = UserService()
    data = UserCreate(**request.get_json())
    try:
        user = service.create(data)
    except EmailAlreadyExists as e:
        return {"error": "email_already_exists", "message": str(e)}, 409
    return UserRead.model_validate(user).model_dump(), 201


@bp.route("", methods=["GET"])
def list_users():
    service = UserService()
    users = service.repository.list()
    return [UserRead.model_validate(user).model_dump() for user in users], 200


@bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    service = UserService()
    try:
        user = service.get(user_id)
    except UserNotFound as e:
        return {"error": "not_found", "message": str(e)}, 404
    return UserRead.model_validate(user).model_dump(), 200


@bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id: int):
    service = UserService()
    data = UserUpdate(**request.get_json())
    try:
        user = service.update(user_id, data)
    except UserNotFound as e:
        return {"error": "not found", "message": str(e)}, 404
    except EmailAlreadyExists as e:
        return {"error": "email_already_exist", "message": str(e)}, 409
    return UserRead.model_validate(user).model_dump(), 200


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    service = UserService()
    try:
        service.delete(user_id)
    except UserNotFound as exc:
        return {"error": "not_found", "message": str(exc)}, 404
    return "", 204
