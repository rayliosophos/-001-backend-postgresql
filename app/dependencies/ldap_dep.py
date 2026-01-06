from app.services.ldap_service import LDAPService

def get_ldap_service() -> LDAPService:
    return LDAPService()