# fastapi_cors.py
#CORS or "Cross-Origin Resource Sharing" 
# refers to the situations when a frontend running in a browser 
# has JavaScript code that communicates with a backend, 
# and the backend is in a different "origin" than the frontend.

#An "origin" is defined as a combination of scheme (http or https),
# host (domain), and port.
#For example, if your frontend is running at http://localhost:3000
# and your backend is running at http://localhost:8000,
# they are considered to be in different origins 
# because of the different ports (3000 vs 8000).

# Use CORS middleware to enable CORS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}