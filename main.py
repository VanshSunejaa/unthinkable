from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload, similar

app = FastAPI()
from fastapi.staticfiles import StaticFiles

# Serve your dataset images and uploaded files to the browser
app.mount("/static", StaticFiles(directory="data/images"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(upload.router, prefix='/api')
# app.include_router(similar.router, prefix="/api")
app.include_router(similar.router, prefix='/api')

@app.get("/")
def home():
    return {"message": "Visual Product Matcher Backend Running 🚀"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
