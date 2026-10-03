## This is just like const express = require('express') in Node.js. It pulls in the main framework.
from fastapi import FastAPI
## This is a security plugin. In JS/Node, you would use app.use(cors()). It controls who is allowed to talk to your API.
from fastapi.middleware.cors import CORSMiddleware

from app.utils.auth import verify_token_middleware

from app.api import api_router

app = FastAPI()

# ⚠️CRITICAL FOR REACT: Allow your React app to access this API
origins = [
    "http://localhost:3000", # Default React port
    "http://localhost:5173", # Default Vite + React port
    "http://localhost:4200", # Default Vite + React port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# 1. Register the separated middleware logic
app.middleware("http")(verify_token_middleware)

# 2. Include the separated routes
app.include_router(api_router  )


 