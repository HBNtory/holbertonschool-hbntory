from flask import Blueprint, render_template, redirect, url_for, request
from pydantic import ValidationError

from app.exceptions.user_exceptions import EmailAlreadyExists, UserNotFound, AdminAlreadyExists
from app.schemas.user import UserCreate, UserUpdate
from app.services.branch_service import BranchService
from app.services.stock import StockService
from app.services.user import UserService

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
def dashboard():
    """Backoffice landing page: entity entry cards with counts (SSR)."""
    counts = {
        "branches": len(BranchService().list()),
        "stock": len(StockService().list()),
        "users": len(UserService().list()),
    }
    return render_template("admin/dashboard.html", counts=counts)

@bp.route("/users", methods=["GET"])
def users_list():
    """List all users (SSR table)."""
    users = UserService().list()
    return render_template("admin/users/list.html", users=users)

@bp.route("/users/<int:user_id>/delete", methods=["POST"])
def users_delete(user_id):
    """Soft-delete a user, then redirect back to the list."""
    UserService().delete(user_id)
    return redirect(url_for("admin.users_list"))

@bp.route("/users/new", methods=["GET", "POST"])
def users_new():
    """Show the create form (GET) or create a user (POST)."""
    branches = BranchService().list()

    if request.method == "POST":
        try:
            data = UserCreate(
                first_name=request.form.get("first_name"),
                last_name=request.form.get("last_name"),
                email=request.form.get("email"),
                password=request.form.get("password"),
                role=request.form.get("role"),
                branch_id=request.form.get("branch_id", type=int),
            )
            UserService().create(data)
        except (ValidationError, EmailAlreadyExists, AdminAlreadyExists) as exc:
            return render_template(
                "admin/users/form.html",
                user=None, branches=branches, error=str(exc),
            )
        return redirect(url_for("admin.users_list"))

    return render_template("admin/users/form.html", user=None, branches=branches)


@bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def users_edit(user_id):
    """Show the edit form (GET) or update a user (POST)."""
    branches = BranchService().list()
    try:
        user = UserService().get(user_id)
    except UserNotFound:
        return redirect(url_for("admin.users_list"))

    if request.method == "POST":
        fields = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "role": request.form.get("role"),
            "branch_id": request.form.get("branch_id", type=int),
        }
        password = request.form.get("password")
        if password:
            fields["password"] = password

        try:
            UserService().update(user_id, UserUpdate(**fields))
        except (ValidationError, EmailAlreadyExists, AdminAlreadyExists) as exc:
            return render_template(
                "admin/users/form.html",
                user=user, branches=branches, error=str(exc),
            )
        return redirect(url_for("admin.users_list"))

    return render_template("admin/users/form.html", user=user, branches=branches)