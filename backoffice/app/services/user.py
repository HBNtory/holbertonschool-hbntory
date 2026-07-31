from app.exceptions.user_exceptions import (EmailAlreadyExists,
                                            UserNotFound,
                                            AdminAlreadyExists)
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.user import UserRepository
from app.utils.security import hash_password


class UserService:
    """Business logic for users: uniqueness, password hashing, soft delete.

    Uses UserRepository for data access (injected). Raises business exceptions.
    It does not deal with HTTP.S
    """

    def __init__(self, repository: UserRepository | None = None):
        """Build the service with a repository (a default one if non given)."""
        self.repository = repository or UserRepository()

    def create(self, data: UserCreate) -> User:
        """Create a user, hashing the password before persistence.

        Returns:
             The created user.
        """
        if data.role == UserRole.admin and self.repository.admin_exists():
            raise AdminAlreadyExists()

        if self.repository.get_by_email(data.email) is not None:
            raise EmailAlreadyExists(data.email)

        user = User(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password_hash=hash_password(data.password),
            role=data.role,
            branch_id=data.branch_id
        )
        return self.repository.create(user)

    def list(self) -> list[User]:
        """Return all users."""
        return self.repository.list()

    def get(self, user_id: int) -> User:
        """Return a user by id

        Returns:
            The matching user.
        """
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user

    def update(self, user_id: int, data: UserUpdate) -> User:
        """Update the provided fields of a user (partial update).

        Re-hashes the password if a new one is provided. Check email
        uniqueness if the email changes.

        Returns:
             The update user.
        """
        user = self.get(user_id)
        fields = data.model_dump(exclude_unset=True)

        if (fields.get("role") == UserRole.admin and
                user.role != UserRole.admin):
            if self.repository.admin_exists():
                raise AdminAlreadyExists()

        if "email" in fields:
            existing = self.repository.get_by_email(fields["email"])
            if existing is not None and existing.id != user.id:
                raise EmailAlreadyExists(fields["email"])

        if "password" in fields:
            user.password_hash = hash_password(fields.pop("password"))

        for key, value in fields.items():
            setattr(user, key, value)

        return self.repository.update(user)

    def delete(self, user_id: int) -> None:
        """Soft-delete a user (set active=False), keeping the row.
        """
        user = self.get(user_id)
        user.active = False
        self.repository.update(user)
