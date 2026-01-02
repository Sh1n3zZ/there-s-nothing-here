from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.documents import router as documents_router
from routes.yt_subtitle import router as yt_subtitle_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router, prefix="/documents", tags=["documents"])
app.include_router(yt_subtitle_router, prefix="/youtube", tags=["youtube"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
