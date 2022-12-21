import os

def strtobool(val):
    val = val.lower()

    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1

    if val in ("n", "no", "f", "false", "off", "0"):
        return 0

    raise ValueError(f"invalid truth value {val}")


def bool_cast(value):
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    if value == "":
        return None

    return bool(strtobool(value))


def gen_secret_key():
    # Attempt to read the secret from the secret file
    # This will fail if the secret has not been written
    try:
        with open(".together_today_secret_key", "rb") as secret:
            key = secret.read()
    except OSError:
        key = None

    if not key:
        key = os.urandom(64)
        # Attempt to write the secret file
        # This will fail if the filesystem is read-only
        try:
            with open(".together_today_secret_key", "wb") as secret:
                secret.write(key)
                secret.flush()
        except OSError:
            pass

    return key


class Config:
    DEBUG: bool = bool_cast(os.environ.get("DEBUG", True))
    SECRET_KEY: str = os.environ.get("SECRET_KEY", gen_secret_key())
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR}/together_today.db",
    )

    UPLOADS_FOLDER = os.path.join(BASE_DIR, "uploads", "profile_pictures")
    PHOTOS_FOLDER = os.path.join(BASE_DIR, "uploads", "photos")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = bool_cast(
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    )
    DEBUG_TB_INTERCEPT_REDIRECTS = False
