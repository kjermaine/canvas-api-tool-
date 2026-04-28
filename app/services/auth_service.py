from collections.abc import Callable

from app.schemas.oauth_provider import OAuthProvider
from app.providers.registry import resolve_provider


class AuthService:
    def __init__(self, provider_resolver: Callable = resolve_provider):
        self.provider_resolver = provider_resolver

    def login_oauth(self, provider: OAuthProvider, payload):
        provider_impl = self.provider_resolver(provider)
        identity = provider_impl.authenticate(payload)

        return {
            "access_token": f"token-for-{identity['email']}",
            "token_type": "bearer",
        }