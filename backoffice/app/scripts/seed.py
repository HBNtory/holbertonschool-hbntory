"""Seed script: populates the DB with initial data (run manually)."""

import os
import random

from app import create_app
from app.exceptions.stock_exceptions import StockAlreadyExists
from app.schemas.stock import StockCreate
from app.services.branch_service import BranchService
from app.services.stock import StockService
from app.services.user import UserService
from app.schemas.branch import BranchCreate
from app.schemas.user import UserCreate
from app.models.user import UserRole
from app.config import Config

QUANTITY_RANGE = (0, 200)


def seed_branches(branch_service: BranchService) -> list:
    labels = ["Lille", "Paris"]
    branches = []
    for label in labels:
        existing = branch_service.repository.get_by_label(label)
        if existing is not None:
            print(f"Branch {label} already exists, skipping.")
            branches.append(existing)
        else:
            branch = branch_service.create(BranchCreate(label=label))
            print(f"Branch {label} created.")
            branches.append(branch)
    return branches


def seed_admin(user_service: UserService, branch_id: int) -> None:
    admin_email = Config.ADMIN_BACKOFFICE_EMAIL
    admin_password = Config.ADMIN_BACKOFFICE_PASSWORD

    if user_service.repository.get_by_email(admin_email) is not None:
        print(f"Admin {admin_email} already exists, skipping.")
        return

    user_service.create(UserCreate(
        first_name="Admin",
        last_name="Backoffice",
        email=admin_email,
        password=admin_password,
        role=UserRole.admin,
        branch_id=branch_id,
    ))
    print(f"Admin {admin_email} created.")


def seed_stocks(stock_service: StockService, branches: list) -> None:
    catalog = stock_service.product_client.list()
    if not catalog:
        print("Product catalog is empty, no stock seeded.")
        return

    created = 0
    skipped = 0
    for product in catalog:
        product_id = product["id"]
        for branch in branches:
            try:
                stock_service.create(StockCreate(
                    branch_id=branch.id,
                    product_id=product_id,
                    quantity=random.randint(*QUANTITY_RANGE),
                ))
                created += 1
            except StockAlreadyExists:
                skipped += 1

    print(f"Stocks seeded: {created} created, {skipped} skipped.")


def seed() -> None:
    branch_service = BranchService()
    user_service = UserService()
    stock_service = StockService()

    branches = seed_branches(branch_service)
    seed_admin(user_service, branches[0].id)
    seed_stocks(stock_service, branches)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
