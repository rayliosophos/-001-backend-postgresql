from app.services.login_service import LoginService

def get_login_service() -> LoginService:
    return LoginService()