# Full Construction ERP System

A comprehensive Enterprise Resource Planning (ERP) system for construction companies.

## Modules

| Module | Features |
|--------|----------|
| **Projects** | Projects, phases, tasks, milestones, client management |
| **Resources** | Equipment tracking, material inventory, allocations, maintenance |
| **Finance** | Budgets, invoices, payments, expense management |
| **Procurement** | Vendors, purchase orders, goods receipts, inventory transactions |
| **HR** | Employees, attendance, leave requests, payroll |
| **Documents** | Document management, versioning, drawing sets |

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework + PostgreSQL
- **Frontend**: React 18 + React Router
- **Auth**: JWT (SimpleJWT)
- **Infrastructure**: Docker Compose + Nginx + Redis + Celery
- **API Docs**: OpenAPI / Swagger (`/api/docs/`)

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env

# 2. Start all services
docker-compose up -d

# 3. Create superuser
docker-compose exec backend python manage.py createsuperuser

# 4. Access the app
# Frontend: http://localhost
# API:      http://localhost/api/
# Admin:    http://localhost/admin/
# API Docs: http://localhost/api/docs/
```

## Development Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## API Endpoints

| Prefix | Description |
|--------|-------------|
| `/api/projects/` | Projects, phases, tasks, milestones, clients |
| `/api/resources/` | Equipment, materials, allocations, maintenance |
| `/api/finance/` | Budgets, invoices, payments, expenses |
| `/api/procurement/` | Vendors, purchase orders, inventory |
| `/api/hr/` | Employees, attendance, leave, payroll |
| `/api/documents/` | Documents, versions, drawing sets |

## Project Structure

```
Full-Construction-ERP-System/
├── backend/
│   ├── erp/              # Django project settings
│   ├── projects/         # Project management
│   ├── resources/        # Equipment & materials
│   ├── finance/          # Financial management
│   ├── procurement/      # Purchasing & inventory
│   ├── hr/               # Human resources
│   ├── documents/        # Document management
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Shared components
│   │   └── services/     # API service layer
│   └── package.json
├── docker-compose.yml
├── nginx.conf
└── .env.example
```

## License

MIT
