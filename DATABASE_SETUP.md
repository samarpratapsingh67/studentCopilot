# PostgreSQL Setup Guide for Netflix Churn Prediction

## STEP 1: PostgreSQL Installation

### Windows Installation

#### Option A: Using PostgreSQL Installer (Recommended)
1. Download from: https://www.postgresql.org/download/windows/
2. Run the installer (postgresql-xx-x64.exe)
3. **IMPORTANT** - When prompted, set a password for the `postgres` user. Remember this password!
4. Installation location: Default is fine (C:\Program Files\PostgreSQL\15)
5. Port: Keep default as 5432
6. Locale: Default is fine
7. Complete installation

#### Option B: Using Chocolatey
```powershell
choco install postgresql
```

#### Option C: Using Miniconda/Conda
```powershell
conda install -c conda-forge postgresql
```

### Verify Installation
```powershell
psql --version
```

---

## STEP 2: Create Database and User

### Start PostgreSQL Server
```powershell
# Windows (if installed via installer)
pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start

# Or use Windows Services to start PostgreSQL
```

### Connect to PostgreSQL
```powershell
psql -U postgres
```
When prompted, enter the password you set during installation.

### Create Database and User (Run in psql)
```sql
-- Create new user
CREATE USER churn_user WITH PASSWORD 'churn_password_123';

-- Create database
CREATE DATABASE churn_prediction;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE churn_prediction TO churn_user;

-- Connect to the database
\c churn_prediction

-- Grant schema privileges
GRANT ALL PRIVILEGES ON SCHEMA public TO churn_user;

-- Exit psql
\q
```

---

## STEP 3: Update requirements.txt

Add these packages to your [requirements.txt](requirements.txt):

```
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-dotenv==1.0.0
alembic==1.13.0
```

### Install them:
```powershell
pip install -r requirements.txt
```

---

## STEP 4: Environment Configuration

Create a `.env` file in the project root:

```env
# PostgreSQL Connection
DATABASE_URL=postgresql+psycopg2://churn_user:churn_password_123@localhost:5432/churn_prediction

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=False

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Port
PORT=5000
```

### Create .env File Safely
```powershell
# From project root
New-Item -Path .env -ItemType File
# Edit with VS Code or your editor
```

---

## STEP 5: Test Connection

Run this Python script to verify DB connection:

```python
# test_db_connection.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(f"Connecting to: {DATABASE_URL.replace(DATABASE_URL.split('@')[0].split('//')[1], 'USER:PASS')}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run it:
```powershell
python test_db_connection.py
```

---

## STEP 6: Common Issues & Solutions

### Issue: "psql: command not found"
**Solution:** Add PostgreSQL to PATH:
```powershell
$env:Path += ";C:\Program Files\PostgreSQL\15\bin"
```
Make it permanent in System Environment Variables.

### Issue: "Server doesn't listen"
**Solution:** Start PostgreSQL service
```powershell
pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
```

### Issue: "Authentication failed for user 'postgres'"
**Solution:** Try default password or reset:
```powershell
psql -U postgres -h localhost
# Default password on fresh install is often blank, just press Enter
```

### Issue: "FATAL: Peer authentication failed"
**Solution:** Edit `C:\Program Files\PostgreSQL\15\data\pg_hba.conf`
Change `peer` to `md5` for localhost connections.

---

## STEP 7: Backup & Restore

### Backup Database
```powershell
pg_dump -U churn_user -d churn_prediction -f backup.sql
```

### Restore Database
```powershell
psql -U churn_user -d churn_prediction -f backup.sql
```

---

## What's Next

Once PostgreSQL is set up and test connection passes, proceed to STEP 2:
- Create SQLAlchemy models for predictions
- Initialize database tables
- Integrate DB layer into prediction pipeline
