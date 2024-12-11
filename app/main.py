import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from .config import get_settings
from .genEmail import register_email_api

# from .graph.tigergraph import get_tg_connection

config = get_settings()

# Creating an app using FastAPI module.
app = FastAPI(title="Mailbox Maverics")

# add gzip middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# The CORS mechanism supports secure cross-origin requests and data transfers between browsers and servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# conn = get_tg_connection()


register_email_api(app)


@app.get("/", tags=["Info"])
def index():
    """Returns info."""
    return f"Mailbox Maverics"


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000, 
        debug=True
    )
