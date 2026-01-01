from pydantic import BaseModel

class RevokeRequest(BaseModel):
    token: str
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str
