
from enum import Enum

class OAuthProvider(str, Enum):
    GOOGLE = "google"
    GITHUB = "github"