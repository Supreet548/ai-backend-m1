from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
import uuid
from app.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        #Generate Request ID
        request_id = str(uuid.uuid4())

        start_time = time.time()

        logger.info(f"[{request_id}] Incoming request: {request.method} {request.url}")

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            f"[{request_id}] Completed response: {response.status_code} in {process_time:.4f}s"
        )

        #Add headers to response
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id

        return response