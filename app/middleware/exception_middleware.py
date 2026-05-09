from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.logger import logger


from fastapi import HTTPException

class ExceptionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)

        except HTTPException as http_exc:
            return JSONResponse(
                status_code=http_exc.status_code,
                content={
                    "success": False,
                    "error": http_exc.detail
                }
            )

        except Exception as e:
            logger.error(f"Unhandled error: {str(e)}")

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Internal Server Error"
                }
            )