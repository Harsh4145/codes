# Medicine Tracking Management System (Flask)

Simple college project to manage medicines, stock, expiry tracking, and transactions.

## Features
- Authentication (login/logout)
- Medicines CRUD
- Stock and expiry alerts
- Purchase/Dispense transactions

## Quickstart
```bash
# 1) Ensure Python 3.10+ and venv support are installed
sudo apt-get update && sudo apt-get install -y python3-venv

# 2) Setup venv and install deps
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3) Initialize DB and run
export FLASK_APP=medtrack/app.py
flask db-upgrade
flask run --host 0.0.0.0 --port 5000
```

Default admin: admin@example.com / admin123