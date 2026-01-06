from .timing import TimingMiddleware
from .cors import add_cors_middleware

def setup_middlewares(app):
    add_cors_middleware(app)
    app.add_middleware(TimingMiddleware)
