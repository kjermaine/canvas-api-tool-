from app.schemas.oauth_provider import OAuthProvider
from app.providers.google import GoogleOAuthProvider
from app.providers.github import GitHubOAuthProvider


PROVIDER_TABLE = {
    OAuthProvider.GOOGLE: GoogleOAuthProvider(),
    OAuthProvider.GITHUB: GitHubOAuthProvider(),
}


def resolve_provider(provider: OAuthProvider):
    try:
        return PROVIDER_TABLE[provider]
    except KeyError:
        raise ValueError(f"Unsupported OAuth provider: {provider}")
