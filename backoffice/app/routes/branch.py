from flask import Blueprint, request

from app.exceptions.branch_exceptions import (DuplicateBranchLabelException,
                                              BranchNotFoundException)
from app.schemas.branch import BranchCreate, BranchRead, BranchUpdate
from app.services.branch_service import BranchService

bp = Blueprint("branch", __name__, url_prefix="/branches")


@bp.route("", methods=["POST"])
def create_branch():
    service = BranchService()
    data = BranchCreate(**request.get_json())
    try:
        branch = service.create(data)
    except DuplicateBranchLabelException as e:
        return {"error": "Duplicate_label", "message": str(e)}, 409
    return BranchRead.model_validate(branch).model_dump(), 201


@bp.route("", methods=["GET"])
def list_branches():
    service = BranchService()
    branches = service.list()
    return [BranchRead.model_validate(branch).model_dump()
            for branch in branches], 200


@bp.route("/<int:branch_id>", methods=["GET"])
def get_branch(branch_id: int):
    service = BranchService()
    try:
        branch = service.get(branch_id)
    except BranchNotFoundException as e:
        return {"error": "not_found", "message": str(e)}, 404
    return BranchRead.model_validate(branch).model_dump(), 200


@bp.route("/<int:branch_id>", methods=["PATCH"])
def update_branch(branch_id: int):
    service = BranchService()
    data = BranchUpdate(**request.get_json())
    try:
        branch = service.update(branch_id, data)
    except BranchNotFoundException as e:
        return {"error": "not_found", "message": str(e)}, 404
    except DuplicateBranchLabelException as e:
        return {"error": "duplicate_branch", "message": str(e)}, 409
    return BranchRead.model_validate(branch).model_dump(), 200


@bp.route("/<int:branch_id>", methods=["DELETE"])
def delete_branch(branch_id: int):
    service = BranchService()
    try:
        service.delete(branch_id)
    except BranchNotFoundException as e:
        return {"error": "not_found", "message": str(e)}, 404
    return "", 204
