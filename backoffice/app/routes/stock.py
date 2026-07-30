from flask import Blueprint, jsonify
from app.services.stock import StockService


bp = Blueprint("stock", __name__, url_prefix="/stocks")

stock_service = StockService()


@bp.route("/<string:branch_label>/<int:product_id>", methods=["GET"])
def get_stock_by_branch_label_and_product_id(
        branch_label: str, product_id: int):
    stock = stock_service.get_stock_by_branch_label_and_product_id(
        branch_label=branch_label, product_id=product_id
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
