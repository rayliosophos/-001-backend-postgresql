import logging
from app.core.config import settings
from ldap3 import Server, Connection, SIMPLE
from ldap3.core.exceptions import LDAPException, LDAPBindError

logger = logging.getLogger(__name__)

class LDAPService:

    @staticmethod
    def authenticate(*, username: str, password: str) -> bool:
        user_dn = f"uid={username},{settings.LDAP_BASE_DN}"
        server = Server(
            settings.LDAP_SERVER,
            port=settings.LDAP_PORT,
            connect_timeout=settings.LDAP_TIMEOUT,
            use_ssl=False, # Set to False for non-SSL connections, Production True
        )
        try:
            conn = Connection(
                server,
                user=user_dn,
                password=password,
                authentication=SIMPLE,
                auto_bind=True,
            )
            return True
        except LDAPBindError:
            logger.warning("Invalid LDAP credentials")
            return False
        except LDAPException as e:
            logger.error("LDAP error", exc_info=e)
            return False
        finally:
            if "conn" in locals() and conn.bound:
                conn.unbind()