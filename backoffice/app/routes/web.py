from flask import Blueprint, render_template, request
import requests

from app.clients.ai_agent import send_to_ai_agent

bp = Blueprint("web", __name__)


def _extract_answer(result: dict) -> str:
    """Pull the answer text out of the ai_service response.

    ⚠️ The ai_service response shape is not finalized yet. Adjust the
    key below once the contract is known (share the ai_service /query
    handler and this becomes exact).
    """
    return result.get("answer", "")


@bp.route("/", methods=["GET", "POST"])
def index():
    """Render the public home page (SSR)."""
    question = None
    answer = None
    error = None

    if request.method == "POST":
        question = (request.form.get("query") or "").strip()
        if not question:
            error = "Please type a question."
        else:
            try:
                result = send_to_ai_agent(question)
                answer = _extract_answer(result)
            except requests.RequestException:
                error = ("The assistant is unavailable right now."
                         " Please try again.")

    return render_template(
        "index.html",
        question=question,
        answer=answer,
        error=error
    )
