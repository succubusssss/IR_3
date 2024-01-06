from fastapi import FastAPI
import uvicorn
from fastapi.responses import PlainTextResponse, FileResponse
from public.router_users import users_router
from datetime import datetime
datetime.utcnow()


app = FastAPI()



#f_bilder()

app.include_router(users_router)
@app.on_event("startup")
def on_startup():
    open("Log_p.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')

@app.on_event("shutdown")
def shutdown():
    open("Log_p.txt", mode="a").write(f'{datetime.utcnow()}: End\n')

@app.get('/')
def main():
    return FileResponse("files/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)