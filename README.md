## Getting Started

### Prerequisites
- Python 3.12+
- Docker
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/o-teu-username/ArticlesManager.git
cd ArticlesManager
```

2. **Create and activate a virtual environment**
```bash
python -m venv env

# Linux/Mac
source env/bin/activate

# Windows
env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

5. **Load the database fixtures**
```bash
python3 manage.py loaddata fixtures/db.json
```

6. **Run the development server**
```bash
python3 manage.py runserver
```

7. **Access the application**

Open your browser and go to `http://localhost:8000`

### Testing the API (Postman)
The backend API is available at `http://localhost:8000`

To test the endpoints:
1. Make a `GET` request to `http://localhost:8000/api/csrf/` to obtain the CSRF token
2. In the **Scripts → Post-response** tab, add:
```javascript
pm.environment.set("csrfToken", pm.cookies.get("csrftoken"));
```
3. Use `{{csrfToken}}` in the `X-CSRFToken` header for all subsequent requests

### Default credentials
| Username | Password | Role |
|----------|----------|------|
| pedro | 123 | Admin |
| joao  | Password123! | Staff |
