from pydantic import BaseModel

class OAuthLoginRequest(BaseModel):
    code: str | None = None
    id_token: str | None = None
    redirect_uri: str | None = None