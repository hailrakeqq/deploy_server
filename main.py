from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import docker

# to run: uvicorn main:app --host 0.0.0.0 --port 25381 --reload

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
client = docker.from_env()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(authorization: str = Header(None)):
    print(f'Auth: {authorization}')
    if not authorization:
        raise HTTPException(401, "Missing auth header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid auth type")
    
    token = authorization.split(" ")[1]
    if token != API_TOKEN:
        raise HTTPException(403, "Invalid token")


@app.get("/")
def deploy(image_name: str, image_tag: str, auth=Depends(verify_token)):

    full_image = f'{image_name}:{image_tag}'
    client.images.pull(image_name, image_tag)
    try:
        old_container = client.containers.get(image_name)
        old_container.stop()
        old_container.remove()
    except docker.errors.NotFound:
        pass

    container = client.containers.run(
        full_image,
        detach=True,
        name=image_name,
        ports={
            "25380/tcp": 25380
        },
        volumes={
            f'{image_name}-volume': {"bind": "/app", "mode": "rw"}
        }
    )

    return {
        "message": "Deploy completed",
        "container_id": container.id
    }