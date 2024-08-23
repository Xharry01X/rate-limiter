from fastapi import FastAPI
from starlette.requests import Request
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import asyncio

app = FastAPI()


# limiter instance
limiter = Limiter(key_func=get_remote_address)

# aading slowapimiddleware to the Fastapi middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

#adding a exception handler for ratelimitexceed errors
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

# rate limit endpoint
@app.get("/rate-limited")
@limiter.limit("5/minute")   #5 request per minute

async def rate_limited_endpoint(request: Request):
    await asyncio.sleep(0.1)
    
    return {"message":"This is rate-limited endpoint"}


@app.get("/non-rate-limited")
async def non_rate_limited_endpoint():
    # Simulate some asynchronous operation
    await asyncio.sleep(0.1)
    
    # Return a message
    return {"message": "This is a non-rate-limited endpoint"}