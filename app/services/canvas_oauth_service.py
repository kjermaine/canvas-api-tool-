import requests


class CanvasOAuthService:
    def build_authorization_url(self, base_url: str, client_id: str, redirect_uri: str, state: str):
        return (
            f"{base_url.rstrip('/')}/login/oauth2/auth"
            f"?client_id={client_id}"
            f"&response_type=code"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
        )

    def exchange_code_for_token(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        code: str,
    ):
        response = requests.post(
            f"{base_url.rstrip('/')}/login/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()