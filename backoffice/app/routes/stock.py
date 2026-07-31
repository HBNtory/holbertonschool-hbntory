import requests
from flask import Blueprint, jsonify, request

from app.exceptions.stock_exceptions import (
    ProductNotFound,
    StockAlreadyExists,
    StockNotFound,
)
from app.schemas.stock import StockCreate, StockRead, StockUpdate
from app.services.stock import StockService

bp = Blueprint("stock", __name__, url_prefix="/stocks")


@bp.route("", methods=["POST"])
def create_stock():
    service = StockService()
    data = StockCreate(**request.get_json())
    try:
        stock = service.create(data)
    except ProductNotFound as e:
        return {"error": "not_found", "message": str(e)}, 422
    except StockAlreadyExists as e:
        return {"error": "stock_already_exist", "message": str(e)}, 409
    except requests.RequestException as e:
        return {
            "error": "product_api_unvailable",
            "message": "The product API is unreachable",
        }, 503
    return StockRead.model_validate(stock).model_dump(), 201


@bp.route("", methods=["GET"])
def list_stock():
    service = StockService()
    branch_id = request.args.get("branch_id", type=int)
    stocks = service.repository.list(branch_id)
    return [StockRead.model_validate(s).model_dump() for s in stocks], 200


@bp.route("/<int:stock_id>", methods=["GET"])
def get_stock(stock_id):
    service = StockService()
    try:
        stock = service.get(stock_id)
    except StockNotFound as exc:
        return {"error": "not_found", "message": str(exc)}, 404
    return StockRead.model_validate(stock).model_dump(), 200


@bp.route("/<int:stock_id>", methods=["PATCH"])
def update_stock(stock_id):
    service = StockService()
    data = StockUpdate(**request.get_json())
    try:
        stock = service.update(stock_id, data)
    except StockNotFound as exc:
        return {"error": "not_found", "message": str(exc)}, 404
    return StockRead.model_validate(stock).model_dump(), 200


@bp.route("/<int:stock_id>", methods=["DELETE"])
def delete_stock(stock_id):
    service = StockService()
    try:
        service.delete(stock_id)
    except StockNotFound as exc:
        return {"error": "not_found", "message": str(exc)}, 404
    return "", 204


stock_service = StockService()


@bp.route("/<string:branch_label>/<int:product_id>", methods=["GET"])
def get_stock_by_branch_label_and_product_id(
    branch_label: str,
    product_id: int,
):
    stock = stock_service.get_stock_by_branch_label_and_product_id(
        branch_label=branch_label,
        product_id=product_id,
    )

    if stock is None:
        return {"message": "No product found"}, 404

    return jsonify({
        "branch_id": stock.branch_id,
        "product_id": stock.product_id,
        "quantity": stock.quantity,
    }), 200


@bp.route("/<string:branch_label>", methods=["GET"])
def get_stock_by_branch(branch_label: str):
    stocks = stock_service.get_stock_by_branch_label(branch_label)
    if not stocks:
        return {"message": "No stock found"}, 404

    return jsonify([
        {
            "branch_id": stock.branch_id,
            "product_id": stock.product_id,
            "quantity": stock.quantity,
        }
        for stock in stocks
    ]), 200
