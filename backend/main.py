from fastapi import FastAPI, Cookie, Form, HTTPException, Request, Response, status
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login")
async def login(request:Request, response: Response, username: str, password:str):
    return True