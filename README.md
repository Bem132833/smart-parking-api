 Smart Parking API

A Smart Parking Management System built with "Django REST Framework".  
Users can find, reserve, and pay for parking spots online.

 Features
- User authentication with JWT  
- Manage parking spots and availability  
- Make and cancel reservations  
- Handle payments securely  
- Admin dashboard for management  


 Tech Stack
- Backend: Django, DRF  
- Authuntication: JWT (SimpleJWT)  
- Database: SQLite / PostgreSQL  
- Docs: Swagger (drf-yasg)  

 Setup

```bash
# 1. Clone the repo
git clone https://github.com/Bem132833/smart-parking-api.git
cd smart-parking-api

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver

API Endpoints 
| Endpoint             | Method | Description        |
| -------------------- | ------ | ------------------ |
| `/api/spots/`        | GET    | List parking spots |
| `/api/reservations/` | POST   | Create reservation |
| `/api/payments/`     | POST   | Make payment       |
| `/api/auth/token/`   | POST   | Get JWT token      |
| `/swagger/`          | GET    | View API docs      |

