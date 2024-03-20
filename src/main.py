from fastapi import FastAPI

from router import router
from router_chat import router as router_chat

app = FastAPI()
app.include_router(
    router,
    prefix='/gpt',
    tags=['Gpt']
)
app.include_router(
    router_chat,
    prefix='/chat',
    tags=['Chat']
)


@app.get("/")
def home():
    return "Welcome"
