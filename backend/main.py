from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.chat import router as chat_router
from routes.tickets import router as tickets_router

app = FastAPI(title="Pin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(tickets_router, prefix="/tickets", tags=["Tickets"])

@app.get("/")
def root():
    return {"message": "Pin FastAPI is running"}
