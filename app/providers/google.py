class GoogleOAuthProvider:
    def authenticate(self, payload):
        # TEMP: mock implementation

        return {
            "email": "google_user@example.com",
            "provider": "google",
        }