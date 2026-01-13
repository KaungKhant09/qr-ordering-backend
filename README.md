# QR Ordering Backend

Backend for a **QR-based self-service buffet ordering system** built with **Django**, **Django REST Framework**, and **PostgreSQL**.

Customers scan a QR code at their table to view the menu and place orders.  
Staff manage and track orders via a separate web interface.

---

## Tech Stack

- Python 3.13
- Django
- Django REST Framework
- PostgreSQL
- GitHub (version control)

---

## Core Features (MVP)

- QR-based table identification
- Buffet plan selection (Basic / Standard / Premium)
- Menu items categorized and plan-restricted
- Backend-enforced ordering rules
- Buffet time tracking (start & expiry)
- Automatic order expiry and auto-close
- Staff order status management
- Django Admin for internal management

---

## Project Structure

```
qr_ordering_backend/
├── config/          # Django project settings
├── restaurants/     # Restaurant data
├── tables/          # Table & QR code logic
├── plans/           # Buffet plans & access rules
├── menu/            # Menu items & categories
├── orders/          # Orders & order items
├── manage.py
└── requirements.txt
```

---

## Setup Instructions (Local)

### 1. Clone the Repository
```bash
git clone https://github.com/KaungKhant09/qr-ordering-backend.git
cd qr-ordering-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/db_name
```

> Note:  
> Local development currently uses SQLite by default.  
> PostgreSQL is used in production (Railway).

---

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Staff Account)
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Backend:
```
http://127.0.0.1:8000/
```

Admin:
```
http://127.0.0.1:8000/admin/
```

---

## API Overview

See **Frontend API Contract** (shared separately).

Main endpoints:
- `GET /api/menu/{qr_token}/`
- `POST /api/orders/`
- `GET /api/staff/orders/`
- `PATCH /api/staff/orders/{id}/status/`

The backend strictly enforces:
- Buffet plan rules
- Category access
- Time limits
- Order expiry

---

## Authentication & Access Control

This project uses **session-based authentication** for staff access.

### Customer Access (No Login Required)

Customers place orders via QR code.  
No authentication is required for:
- `GET /api/menu/{qr_token}/`
- `POST /api/orders/`

### Staff Access (Login Required)

Staff must log in via Django Admin:
```
/admin/
```

After login, staff can access:
- `GET /api/staff/orders/`
- `PATCH /api/staff/orders/{id}/status/`

Unauthenticated access to staff endpoints will return **403 Forbidden**.

---

## Development Notes

- Do **not** manually create database tables  
  → Schema is managed via Django models and migrations
- Business rules are enforced at the **API layer**
- Django Admin bypasses business rules and is intended for internal use only

---

## Out of Scope (MVP)

- Customer authentication
- Payments
- Order cancellation
- Real-time updates (WebSockets)
- Role-based staff permissions (beyond basic staff login)

---

## License

Private / Educational Project
