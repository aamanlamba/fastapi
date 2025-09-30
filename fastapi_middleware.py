# fastapi_middleware.py
### A "middleware" is a function that works with every request before it is processed by any specific path operation. And also with every response before returning it.

from fastapi import FastAPI, Request
import time
app = FastAPI()

### The add_process_time_header function is a middleware that prints messages before and after processing each request. The call_next function is used to call the next middleware or the actual path operation.
### You can add as many middlewares as you want, and they
### will be
### executed in the order they are added.
### Middlewares are useful for tasks like logging, authentication, and modifying requests or responses globally.
### Note: Middlewares are different from dependencies. Dependencies are specific to path operations, while middlewares apply to all requests and responses.
### Also, middlewares are executed before dependencies.
### Example: Adding a custom header to all responses
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # Code to be executed for each request before the path operation is called
    print("Before request")
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    # Code to be executed for each response before returning it
    response.headers["X-Custom-Header"] = "Custom value"
    print("After request, process time: ", process_time)
    
    return response

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

