from fastapi import FastAPI
from task import router as task_router
from user import router as user_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to Taskmanager"}


app.include_router(task_router)
app.include_router(user_router)
