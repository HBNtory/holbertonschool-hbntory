from sqlalchemy import select

from app.database import SessionLocal
from app.models.user import User, UserRole


class UserRepository:
    """Data-access layer for the User entity.

    The only place that talks to the ORM for users. Methods run queries and
    return User objects (or None). They contain no business logic and no HTTP.
    """

    def create(self, user: User) -> User:
        """Persist a new user.

        Returns:
             The created user, refreshed with its generated id and timestamps.
        """
        local_session = SessionLocal()
        local_session.add(user)
        local_session.commit()
        local_session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User:
        """Return a user by primary key, or None if not found.

        Returns:
            The matching User, or None
        """
        local_session = SessionLocal()
        return local_session.get(User, user_id)

    def get_by_email(self, user_email: str) -> User:
        """Return a user by email, or None if not found.

        Returns:
            The matching User, or None
        """
        local_session = SessionLocal()
        statement = select(User).where(User.email == user_email)
        return local_session.scalars(statement).first()

    def list(self, include_inactive: bool = False) -> list[User]:
        """List users, excluding soft-deleted ones by default.

        Returns:
            A list of User objects.
        """
        local_session = SessionLocal()
        statement = select(User)
        if not include_inactive:
            statement = statement.where(User.active.is_(True))
        return list(local_session.scalars(statement).all())

    def update(self, user: User) -> User:
        """Persist changes made to a user by the service.

        The service modifies the user's attributes, this commit them.

        Returns:
            The updated user, refreshed with the new updated_at.
        """
        local_session = SessionLocal()
        local_session.commit()
        local_session.refresh(user)
        return user

    def admin_exists(self) -> bool:
        """Return True if an active admin already exists."""
        local_session = SessionLocal()
        statement = select(User).where(
            User.role == UserRole.admin,
            User.active.is_(True),
        )
        return local_session.scalars(statement).first() is not None