from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_hasher = PasswordHasher()

def hash_password(plain_password: str) -> str:
    """Hash a plaintext password with Argon2id.
     Returns:
         The hash string. (algorithm, parameters, salt and hash combined)
    """
    return _hasher.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plaintext password against an Argon2 hash
    Returns:
        True if the password matches, False otherwise.
    """
    try:
        return _hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False