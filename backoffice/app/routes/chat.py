from flask import Blueprint, jsonify, request
from app.services.ai_agent import send_to_ai_agent

bp = Blueprint("chat", __name__)


@bp.route("/chat", methods=["POST"])
def post_chat_message():
    """route to post chat message and get answered back"""
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"message": "The 'query' field can not be empty"}), 400

    answer = send_to_ai_agent(query)
    return jsonify(answer), 200
