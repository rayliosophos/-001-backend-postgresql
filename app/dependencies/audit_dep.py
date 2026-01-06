from app.services.audit_service import AuditService

def get_audit_service() -> AuditService:
    return AuditService()