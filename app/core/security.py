import jwt
from app.core.config import settings
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"

def create_access_token(subject: str, jti: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "iss": settings.ISSUER,
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS),
        "jti": jti,
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[ALGORITHM],
    )
