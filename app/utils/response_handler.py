from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime
from typing import Any, Optional

class ResponseHandler:
    FORMAT = "%d-%B-%Y %H:%M:%S"

    def __init__(self):
        raise RuntimeError("Utility class should not be instantiated")

    @staticmethod
    def _generate_response(
        http_status: int,
        is_success: bool,
        message: str,
        data: Optional[Any]
    ) -> JSONResponse:
        response = {
            "time": datetime.now().strftime(ResponseHandler.FORMAT),
            "status": http_status,
            "isSuccess": is_success,
            "message": message,
            "data": data
        }
        return JSONResponse(
            status_code=http_status,
            content=response
        )

    @staticmethod
    def generate_response_successful(message: str, data: Any) -> JSONResponse:
        return ResponseHandler._generate_response(
            status.HTTP_200_OK,
            True,
            message,
            data
        )

    @staticmethod
    def generate_response_unsuccessful(http_status: int, message: str) -> JSONResponse:
        return ResponseHandler._generate_response(
            http_status,
            False,
            message,
            None
        )
