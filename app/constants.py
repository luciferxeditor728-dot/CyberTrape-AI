"""Application constants."""

# User Roles
USER_ROLES = {
    'ADMIN': 'admin',
    'ANALYST': 'analyst',
    'OPERATOR': 'operator',
    'VIEWER': 'viewer',
    'USER': 'user',
}

# User Roles List
ROLE_LIST = list(USER_ROLES.values())

# Permissions
PERMISSIONS = {
    'USER_CREATE': 'user_create',
    'USER_READ': 'user_read',
    'USER_UPDATE': 'user_update',
    'USER_DELETE': 'user_delete',
    'HONEYPOT_CREATE': 'honeypot_create',
    'HONEYPOT_READ': 'honeypot_read',
    'HONEYPOT_UPDATE': 'honeypot_update',
    'HONEYPOT_DELETE': 'honeypot_delete',
    'ATTACK_READ': 'attack_read',
    'ATTACK_ANALYZE': 'attack_analyze',
    'ALERT_READ': 'alert_read',
    'ALERT_MANAGE': 'alert_manage',
    'ANALYTICS_READ': 'analytics_read',
    'ADMIN_ACCESS': 'admin_access',
    'AUDIT_READ': 'audit_read',
    'BACKUP_CREATE': 'backup_create',
    'BACKUP_RESTORE': 'backup_restore',
}

# Activity Types
ACTIVITY_TYPES = {
    'LOGIN': 'login',
    'LOGOUT': 'logout',
    'USER_CREATE': 'user_create',
    'USER_UPDATE': 'user_update',
    'USER_DELETE': 'user_delete',
    'HONEYPOT_DEPLOYED': 'honeypot_deployed',
    'HONEYPOT_STOPPED': 'honeypot_stopped',
    'ATTACK_DETECTED': 'attack_detected',
    'ALERT_TRIGGERED': 'alert_triggered',
    'REPORT_GENERATED': 'report_generated',
    'BACKUP_CREATED': 'backup_created',
    'SETTINGS_CHANGED': 'settings_changed',
}

# Alert Severity Levels
ALERT_SEVERITY = {
    'CRITICAL': 'critical',
    'HIGH': 'high',
    'MEDIUM': 'medium',
    'LOW': 'low',
    'INFO': 'info',
}

# Alert Status
ALERT_STATUS = {
    'NEW': 'new',
    'IN_PROGRESS': 'in_progress',
    'RESOLVED': 'resolved',
    'IGNORED': 'ignored',
}

# Attack Types
ATTACK_TYPES = {
    'BRUTE_FORCE': 'brute_force',
    'SCANNING': 'scanning',
    'EXPLOIT': 'exploit',
    'MALWARE': 'malware',
    'DATA_EXFILTRATION': 'data_exfiltration',
    'DOS': 'dos',
    'UNKNOWN': 'unknown',
}

# Honeypot Types
HONEYPOT_TYPES = {
    'SSH': 'ssh',
    'HTTP': 'http',
    'FTP': 'ftp',
    'TELNET': 'telnet',
    'SMTP': 'smtp',
    'DNS': 'dns',
    'MYSQL': 'mysql',
    'CUSTOM': 'custom',
}

# Honeypot Status
HONEYPOT_STATUS = {
    'ACTIVE': 'active',
    'INACTIVE': 'inactive',
    'PAUSED': 'paused',
    'ERROR': 'error',
    'OFFLINE': 'offline',
}

# Notification Types
NOTIFICATION_TYPES = {
    'ALERT': 'alert',
    'INFO': 'info',
    'WARNING': 'warning',
    'ERROR': 'error',
    'SUCCESS': 'success',
}

# Notification Channels
NOTIFICATION_CHANNELS = {
    'EMAIL': 'email',
    'SLACK': 'slack',
    'WEBHOOK': 'webhook',
    'DASHBOARD': 'dashboard',
    'SMS': 'sms',
}

# HTTP Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_500_INTERNAL_SERVER_ERROR = 500

# Response Messages
RESPONSE_MESSAGES = {
    'SUCCESS': 'Operation successful',
    'ERROR': 'An error occurred',
    'NOT_FOUND': 'Resource not found',
    'UNAUTHORIZED': 'Unauthorized access',
    'FORBIDDEN': 'Access forbidden',
    'INVALID_INPUT': 'Invalid input provided',
    'ALREADY_EXISTS': 'Resource already exists',
}
