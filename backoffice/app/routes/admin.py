import requests
from flask import Blueprint, render_template, redirect, url_for, request, g
from pydantic import ValidationError

from app.exceptions.branch_exceptions import BranchNotFoundException, DuplicateBranchLabelException, BranchNotEmpty
from app.exceptions.stock_exceptions import ProductNotFound, StockAlreadyExists, StockNotFound
from app.exceptions.user_exceptions import EmailAlreadyExists, UserNotFound, AdminAlreadyExists
from app.schemas.branch import BranchUpdate, BranchCreate
from app.schemas.stock import StockCreate, StockUpdate
from app.schemas.user import UserCreate, UserUpdate
from app.services.branch_service import BranchService
from app.services.stock import StockService
from app.services.user import UserService
from app.utils.helpers import catalog_or_empty, product_names
from app.utils.auth_guard import login_required, roles_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
@login_required
def dashboard():
    """Backoffice landing page: entity entry cards with counts (SSR)."""
    role = g.user["role"]
    counts = {
        "branches": len(BranchService().list()),
        "stock": len(StockService().list()),
        "users": len(UserService().list()),
    }
    return render_template("admin/dashboard.html", counts=counts, role=role)

@bp.route("/users", methods=["GET"])
@roles_required("admin")
def users_list():
    """List all users (SSR table)."""
    users = UserService().list()
    return render_template("admin/users/list.html", users=users)

@bp.route("/users/<int:user_id>/delete", methods=["POST"])
@roles_required("admin")
def users_delete(user_id):
    """Soft-delete a user, then redirect back to the list."""
    UserService().delete(user_id)
    return redirect(url_for("admin.users_list"))

@bp.route("/users/new", methods=["GET", "POST"])
@roles_required("admin")
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
@roles_required("admin")
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

@bp.route("/branches", methods=["GET"])
@roles_required("admin")
def branches_list():
    """List all branches (SSR table)."""
    branches = BranchService().list()
    return render_template("admin/branches/list.html", branches=branches)

@bp.route("/branches/new", methods=["GET", "POST"])
@roles_required("admin")
def branches_new():
    """Show the create form (GET) or create a branch (POST)."""
    if request.method == "POST":
        try:
            data = BranchCreate(label=request.form.get("label"))
            BranchService().create(data)
        except (ValidationError, DuplicateBranchLabelException) as exc:
            return render_template(
                "admin/branches/form.html", branch=None, error=str(exc),
            )
        return redirect(url_for("admin.branches_list"))

    return render_template("admin/branches/form.html", branch=None)


@bp.route("/branches/<int:branch_id>/edit", methods=["GET", "POST"])
@roles_required("admin")
def branches_edit(branch_id):
    """Show the edit form (GET) or update a branch (POST)."""
    try:
        branch = BranchService().get(branch_id)
    except BranchNotFoundException:
        return redirect(url_for("admin.branches_list"))

    if request.method == "POST":
        try:
            data = BranchUpdate(label=request.form.get("label"))
            BranchService().update(branch_id, data)
        except (ValidationError, DuplicateBranchLabelException) as exc:
            return render_template(
                "admin/branches/form.html", branch=branch, error=str(exc),
            )
        return redirect(url_for("admin.branches_list"))

    return render_template("admin/branches/form.html", branch=branch)


@bp.route("/branches/<int:branch_id>/delete", methods=["POST"])
@roles_required("admin")
def branches_delete(branch_id):
    """Delete a branch, unless it still has users or stock."""
    try:
        BranchService().delete(branch_id)
    except BranchNotEmpty as exc:
        # deletion refused: branch has dependents
        return redirect(url_for("admin.branches_list"))
    except BranchNotFoundException:
        return redirect(url_for("admin.branches_list"))
    return redirect(url_for("admin.branches_list"))

@bp.route("/stock", methods=["GET"])
@roles_required("employee")
def stock_index():
    """Stock landing: pick a branch to view its stock."""
    branches = BranchService().list()
    return render_template("admin/stock/branches.html", branches=branches)

@bp.route("/stock/<int:branch_id>", methods=["GET"])
@roles_required("employee")
def stock_detail(branch_id):
    """Show the stock lines of one branch, with product names."""
    try:
        branch = BranchService().get(branch_id)
    except BranchNotFoundException:
        return redirect(url_for("admin.stock_index"))

    stocks = StockService().list(branch_id=branch_id)
    names = product_names()   # dict {id: name}, or None if API unreachable

    return render_template(
        "admin/stock/detail.html",
        branch=branch,
        stocks=stocks,
        names=names,
    )

@bp.route("/stock/<int:branch_id>/new", methods=["GET", "POST"])
@roles_required("employee")
def stock_new(branch_id):
    """Show the create form (GET) or create a stock line (POST)."""
    try:
        branch = BranchService().get(branch_id)
    except BranchNotFoundException:
        return redirect(url_for("admin.stock_index"))

    if request.method == "POST":
        try:
            data = StockCreate(
                branch_id=branch_id,
                product_id=request.form.get("product_id", type=int),
                quantity=request.form.get("quantity", type=int),
            )
            StockService().create(data)
        except (ValidationError, ProductNotFound, StockAlreadyExists) as exc:
            products = catalog_or_empty()
            return render_template(
                "admin/stock/form.html",
                stock=None, branch=branch, products=products, error=str(exc),
            )
        except requests.RequestException:
            products = catalog_or_empty()
            return render_template(
                "admin/stock/form.html",
                stock=None, branch=branch, products=products,
                error="Product API unreachable, try again later.",
            )
        return redirect(url_for("admin.stock_detail", branch_id=branch_id))

    products = catalog_or_empty()
    return render_template(
        "admin/stock/form.html", stock=None, branch=branch, products=products,
    )


@bp.route("/stock/<int:branch_id>/<int:stock_id>/edit", methods=["GET", "POST"])
@roles_required("employee")
def stock_edit(branch_id, stock_id):
    """Show the edit form (GET) or update a stock line's quantity (POST)."""
    try:
        branch = BranchService().get(branch_id)
        stock = StockService().get(stock_id)
    except (BranchNotFoundException, StockNotFound):
        return redirect(url_for("admin.stock_index"))

    if request.method == "POST":
        try:
            data = StockUpdate(quantity=request.form.get("quantity", type=int))
            StockService().update(stock_id, data)
        except (ValidationError, StockNotFound) as exc:
            return render_template(
                "admin/stock/form.html",
                stock=stock, branch=branch, products=[], error=str(exc),
            )
        return redirect(url_for("admin.stock_detail", branch_id=branch_id))

    return render_template(
        "admin/stock/form.html", stock=stock, branch=branch, products=[],
    )


@bp.route("/stock/<int:branch_id>/<int:stock_id>/delete", methods=["POST"])
@roles_required("employee")
def stock_delete(branch_id, stock_id):
    """Hard-delete a stock line, then back to the branch detail."""
    try:
        StockService().delete(stock_id)
    except StockNotFound:
        pass
    return redirect(url_for("admin.stock_detail", branch_id=branch_id))