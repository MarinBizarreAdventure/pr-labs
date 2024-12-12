from fastapi import FastAPI
from app.infrastructure.database.db import DB
from app.infrastructure.repositories.user_repository import UserRepository
from app.presentation.api.v1.user.user_routes import UserRouter
from app.application.services.user_service import UserService

app = FastAPI()

db = DB()

@app.on_event("startup")
def startup_event():
    connection_status = db.check_connection_status()
    print("Connection Status:", connection_status)
    db.create_tables()
    print("Tables created", connection_status)


user_repository = UserRepository(db)
user_service = UserService(user_repository)
user_router = UserRouter(user_service)
app.include_router(user_router.router, prefix="/api/v1", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}

