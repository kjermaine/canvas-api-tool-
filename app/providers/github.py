class GitHubOAuthProvider:
    def authenticate(self, payload):
        return {
            "email": "github_user@example.com",
            "provider": "github",
        }