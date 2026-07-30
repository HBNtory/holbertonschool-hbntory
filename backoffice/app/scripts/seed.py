"""Seed script: populates the DB with initial data (run manually)."""

import os

from app import create_app
from app.services.branch_service import BranchService
from app.services.user import UserService
from app.schemas.branch import BranchCreate
from app.schemas.user import UserCreate
from app.models.user import UserRole
from app.config import Config


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


def seed() -> None:
    branch_service = BranchService()
    user_service = UserService()

    branches = seed_branches(branch_service)
    seed_admin(user_service, branches[0].id)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
