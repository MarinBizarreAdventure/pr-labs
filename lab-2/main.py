import threading
from fastapi import FastAPI
from app.infrastructure.database.db import DB
from app.infrastructure.repositories.user_repository import UserRepository
from app.presentation.api.v1.user.user_routes import UserRouter  
from app.application.services.user_service import UserService
from app.application.services.chat_service import ChatService
from app.presentation.api.v1.user.char_router import ChatRouter, tcp_server, handle_client 

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

chat_service = ChatService()
chat_router = ChatRouter(chat_service)

app.include_router(user_router.router, prefix="/api/v1", tags=["users"])
app.include_router(chat_router.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management and Chat API"}

def start_http_server():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



if __name__ == "__main__":
    http_thread = threading.Thread(target=start_http_server)
    tcp_thread = threading.Thread(target=tcp_server)

    http_thread.start()
    tcp_thread.start()

    http_thread.join()
    tcp_thread.join()



# from fastapi import FastAPI
# from app.infrastructure.database.db import DB
# from app.infrastructure.repositories.user_repository import UserRepository
# from app.presentation.api.v1.user.user_routes import UserRouter
# from app.application.services.user_service import UserService

# app = FastAPI()

# db = DB()

# @app.on_event("startup")
# def startup_event():
#     connection_status = db.check_connection_status()
#     print("Connection Status:", connection_status)
#     db.create_tables()
#     print("Tables created", connection_status)


# user_repository = UserRepository(db)
# user_service = UserService(user_repository)
# user_router = UserRouter(user_service)
# app.include_router(user_router.router, prefix="/api/v1", tags=["users"])

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the User Management API"}

