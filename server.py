from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api import auth

app = FastAPI(title='Omega To-do')

app.include_router(auth.router)

@app.get('/')
async def root():
    return HTMLResponse(content='<h3>Hello World</h3>', status_code=200)