from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
#from public.users import users_router
from datetime import datetime
from db import create_tables

#app = FastAPI()

#app.include_router(users_router)

create_tables()
"""@app.get('/', response_class=PlainTextResponse)
def f_indexH():
    return "<b> Hello, User! </b>"""