from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web import explorer, creature, user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

@app.get("/")
def top():
    return "top here"

@app.get("/echo/{thing}")
def echo(thing: str):
    return f"echoing {thing}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True )