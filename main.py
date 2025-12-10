from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controller import audio_controller

app = FastAPI(title="VIBE Music Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(audio_controller.router, prefix="/api", tags=["audio"])

@app.get("/")
def read_root():
    return {"message": "VIBE Music Recommendation API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
