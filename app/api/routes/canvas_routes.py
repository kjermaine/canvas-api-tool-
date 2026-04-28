
"""
1. make fast api blank startup with uvicorn

2. wire an endpoint to oath request 



GET https://<canvas-install-url>/login/oauth2/auth?client_id=XXX&response_type=code&redirect_uri=https://example.com/oauth_complete&state=YYY&scope=<value_1>%20<value_2>%20<value_n>


import the auth provider 





"""


from fastapi import APIRouter, Depends
from app.api.dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.api.dependencies import get_auth_service
from app.schemas.oauth_provider import OAuthProvider
from app.schemas.auth.auth_request import  OAuthLoginRequest
from app.schemas.auth.auth_response import AuthResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/oauth/google", response_model=AuthResponse)
def login_google(payload: OAuthLoginRequest, service: AuthService = Depends(get_auth_service)):
  
  return service.login_oauth(OAuthProvider.GOOGLE, payload)


@router.post("/oauth/github", response_model = AuthResponse)
def login_github(payload : OAuthLoginRequest, service :AuthService = Depends(get_auth_service)):
     
  return service.login_oauth(OAuthProvider.GITHUB , payload)