import httpx

from urllib.parse import urlencode

from environment import Env
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, Response, HTMLResponse
#import secrets

Env.load()
Env.load("discordia")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
SCOPES  = ["identify"]

Env.list()

@router.get("/")
async def index(request: Request):
    return HTMLResponse("Auth OK")

@router.get("/login")
async def login(request: Request):
    # state = secrets.token_urlsafe(32)
    # request.session["oauth_state"] = state

    params = {
        "client_id": Env.OMEGON_CLIENT_ID,
        "redirect_uri": Env.OMEGON_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        # "state": state,
        "prompt": "consent",
    }
    
    return RedirectResponse(f"{Env.DISCORD_AUTH_URL}?{urlencode(params)}")


@router.get("/callback/")
async def callback(request: Request, code: str, state: str):
    if not code or not state:
        raise HTTPException(400, "Missing code/state")

    # if state != request.session.get("oauth_state"):
    #     raise HTTPException(400, "Invalid state")
    
    data = {
        "client_id": Env.OMEGON_CLIENT_ID,
        "client_secret": Env.OMEGON_TOKEN,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": Env.OMEGON_REDIRECT_URI,
    }

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            Env.DISCORD_TOKEN_URL,
            data=data,
            headers={"Content-Type":"application/x-www-form-urlencoded"}
        )

        if token_resp.status_code != 200:
            raise HTTPException(400, f"Token exchange failed: {token_resp.text}")
        
        token_json = token_resp.json()
        access_token = token_json["access_token"]
        token_type = token_json.get("token_type", "Bearer")

        # pega dados do usuário
        me_resp = await client.get(
            Env.DISCORD_ME_URL,
            headers={"Authorization": f"{token_type} {access_token}"}
        )

        if me_resp.status_code != 200:
            raise HTTPException(400, f"Failed to fetch user: {me_resp.text}")
        me = me_resp.json()

    return Response(me)