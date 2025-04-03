from fastapi import FastAPI
from app.api import routes

# Quantum Computing System is a project for execytubg Quantum circuits.
# API endpoints are handled Asyncronly


# Main.py single responsibility is initilizing the Router of FastAPI.
app = FastAPI()
app.include_router(routes.router)
