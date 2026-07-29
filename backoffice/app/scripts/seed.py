from app.services.branch_service import BranchService


def seed_branches(branch_service: BranchService) -> list:
    labels = ["Lille", "Paris"]
    branches = []

    for label in labels:
        existing = branch_service.repository.get_