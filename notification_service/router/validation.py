from fastapi import APIRouter, Response, status, HTTPException
from fastapi.responses import JSONResponse
import resend
from schema.otp import CreateUser
import secrets 
from database.redis_setup import redis_client
import json
from dotenv import load_dotenv
import os

routers = APIRouter()
load_dotenv()
resend_api_key = os.getenv('RESEND_API_KEY')

@routers.post('/generate-otp')
async def send_otp(user: CreateUser):
    resend.api_key = resend_api_key
    otp = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    try:
        response = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": user.email,
        "subject": "Hello from Python",
        "html": f"<h1>Hello!</h1><p>here is your otp { otp }.</p>",
    })
    except Exception:
        raise HTTPException(
        status_code=500,
        detail="Failed to send OTP"
    )
    await redis_client.set(f"signup:{user.email}",
        json.dumps({
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "otp": otp
    }),ex=100)
    return {'message':'stored in redis successfully'}