from fastapi import FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging
from contextlib import asynccontextmanager
from database import init, init_db  # Adjust import as necessary
from routes import router as api_router

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init()
        yield
    finally:
        # Cleanup code here
        pass

def create_app() -> FastAPI:
    app = FastAPI()

    @app.on_event("startup")
    async def startup_event():
        await init()  # This initializes your database
    app.include_router(api_router)

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        details = exc.errors()
        modified_details = [{"loc": error["loc"], "message": error["msg"], "type": error["type"]} for error in details]
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder({"detail": modified_details}))

    @app.middleware("http")
    async def check_path(request: Request, call_next):
        path = request.url.path
        if any(char in path for char in "`@$#%^*=<>[]|\\~"):
            return JSONResponse({"error": "Invalid path format"}, status_code=400)
        response = await call_next(request)
        return response
    @app.get("/")
    async def root():
        return {"message": "Tomato"}
    
    return app

async def init_app() -> FastAPI:
    """
    Initialise a FastApi app, with all the required routes and the
    :return: FastAPI initialized app
    """
    app_ = FastAPI()
    app_.include_router(api_router)
    init_db(app_)
    @app_.on_event("startup")
    async def start_db():
       await  init_db(app_)


    return app_


app = init_app()