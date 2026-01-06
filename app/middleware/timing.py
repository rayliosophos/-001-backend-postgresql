import time
import logging
import uuid
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("timing")

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        request.state.trace_id = str(uuid.uuid4())
        logger.info("Request %s started: %s %s", request.state.trace_id, request.method, request.url.path)
        response = await call_next(request)
        logger.info("Request %s completed: %s %s | status=%d | duration=%.4f seconds", request.state.trace_id, request.method, request.url.path, response.status_code, time.perf_counter() - start)
        return response