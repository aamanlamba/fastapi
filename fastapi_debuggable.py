# fastapi_debuggable.py
# run in python debugger 

from typing import Annotated
import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


def write_notification(message: str):
    with open("log.txt", mode="w") as email_file:
        email_file.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}"
        background_tasks.add_task(write_notification, message)
    return q

@app.get("/")
async def read_root():
    return {"Hello": "World"}   

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks,
                            q: Annotated[str , Depends(get_query)] = None):
    message = f"message to {email}: {q}"
    background_tasks.add_task(write_notification, message)
    return {"message": "Notification sent in the background"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)