# CyberTrap-AI: Honeypot-Based Attack Intelligence Platform

Advanced cybersecurity platform using honeypots to detect, analyze, and respond to cyber attacks.

## Features

- **Multi-Honeypot Support**: SSH, HTTP, FTP, Telnet, SMTP, DNS, MySQL
- **Real-time Attack Detection**: Monitor and analyze attack patterns
- **User Management**: Role-based access control (RBAC)
- **Two-Factor Authentication**: Enhanced security with 2FA
- **API-First Architecture**: RESTful API for programmatic access
- **Analytics Dashboard**: Comprehensive attack analytics
- **Audit Logging**: Complete audit trail for compliance
- **Backup & Recovery**: Automated backup and restore functionality
- **Notifications**: Real-time alerts via email, Slack, webhooks
- **Session Management**: Track and manage user sessions

## Technology Stack

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Cache**: Redis
- **Queue**: Celery with Redis
- **Frontend**: Bootstrap 5, Jinja2
- **Authentication**: JWT, PyOTP (2FA)
- **Server**: Gunicorn, Nginx
- **Containerization**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd CyberTrape-AI
```

2. **Copy environment file**
```bash
cp .env.example .env
```

3. **Start with Docker Compose**
```bash
docker-compose up -d
```

4. **Initialize database**
```bash
docker-compose exec web flask init-db
docker-compose exec web flask seed-db
```

5. **Access the application**
- Web UI: http://localhost
- API: http://localhost/api/v1
- Default credentials: `admin` / `Admin@123456`

### Development Setup

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
```

4. **Initialize database**
```bash
flask init-db
flask seed-db
```

5. **Run development server**
```bash
flask run
```

## API Documentation

### Authentication

**POST** `/api/v1/auth/login`
```json
{
  "username": "admin",
  "password": "password"
}
```

**Response**
```json
{
  "success": true,
  "user": {...},
  "tokens": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "Bearer"
  }
}
```

### Users

**GET** `/api/v1/users` - Get all users (Admin only)
**GET** `/api/v1/users/{user_id}` - Get user details
**PUT** `/api/v1/users/{user_id}` - Update user
**DELETE** `/api/v1/users/{user_id}` - Delete user

### Analytics

**GET** `/api/v1/analytics/dashboard` - Dashboard data
**GET** `/api/v1/analytics/attacks` - Attack statistics
**GET** `/api/v1/analytics/threats` - Threat data

## Directory Structure

```
CyberTrape-AI/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── constants.py
│   ├── extensions.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── utils/
│   ├── tasks/
│   └── migrations/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
├── .env.example
├── .gitignore
└── README.md
```

## Configuration

Key environment variables:

- `FLASK_ENV`: development, production, testing
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection URL
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT signing key
- `MAIL_*`: Email configuration

## Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Deployment

### Docker Production Build

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```

### Environment Setup

Update `.env` with production values:

```bash
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<generate-secure-key>
JWT_SECRET_KEY=<generate-secure-key>
```

## Security

- All passwords are hashed using bcrypt
- JWT tokens with configurable expiration
- CSRF protection on all forms
- SQL injection prevention via SQLAlchemy ORM
- Rate limiting on API endpoints
- Secure session management
- 2FA support with TOTP

## Monitoring

- Centralized logging to file and console
- Activity logs for all user actions
- Audit logs for system changes
- Redis monitoring
- Celery task monitoring

## Contributing

1. Create a feature branch: `git checkout -b feature/name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/name`
4. Create Pull Request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
