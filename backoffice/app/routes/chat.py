from flask import Blueprint, jsonify, requests

bp = Blueprint("chat", __name__)


@bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"message": "The 'query' field can not be empty"}), 400

    response = request.post("http://ai_service:8000/query", json={"query": query})
    return jsonify(response), response.status_code