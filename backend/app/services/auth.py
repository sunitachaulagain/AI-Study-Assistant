from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.auth import UserRegister
from backend.app.core.security import hash_password


def register_user(db: Session, user_data: UserRegister) -> User:
    # Check if the email is already registered
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already registered")

    # Hash the password before storing it
    hashed_password = hash_password(user_data.password)

    # Create the database user
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user