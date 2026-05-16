"""
Test script to verify PostgreSQL database connection.
Run this to ensure DB setup is correct before running the app.

Usage: python test_db_connection.py
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_connection():
    """Test database connection."""
    print("🔍 Testing PostgreSQL Database Connection...\n")
    
    from src.database.db_config import engine, DATABASE_URL
    
    # Display connection details (without password)
    safe_url = DATABASE_URL.replace(
        DATABASE_URL.split('@')[0],
        'postgresql+psycopg2://USER:***'
    ) if '@' in DATABASE_URL else DATABASE_URL
    
    print(f"📍 Connection String: {safe_url}")
    print()
    
    try:
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database Connection: SUCCESS")
            print()
            
            # Test creating tables
            print("📋 Initializing Database Tables...")
            from src.database.db_config import init_db
            init_db()
            print("✅ Tables Created/Verified Successfully")
            print()
            
            # Display table info
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            
            tables = result.fetchall()
            print(f"📊 Tables in Database ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
            
            print()
            print("✅ All checks passed! Database is ready to use.")
            return True
            
    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}")
        print()
        print("⚠️  Troubleshooting:")
        print("   1. Verify PostgreSQL server is running")
        print("   2. Check DATABASE_URL in .env file")
        print("   3. Verify username and password are correct")
        print("   4. Ensure database 'churn_prediction' exists")
        print()
        print("💡 See DATABASE_SETUP.md for detailed setup instructions")
        return False


def test_services():
    """Test database service layer."""
    print("\n" + "="*50)
    print("🧪 Testing Database Service Layer...")
    print("="*50 + "\n")
    
    try:
        from src.database.services import PredictionService, MetricsService
        print("✅ Database services imported successfully")
        print("   - PredictionService: ✓")
        print("   - MetricsService: ✓")
        return True
    except Exception as e:
        print(f"❌ Service import failed: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  CHURN PREDICTION - DATABASE TEST")
    print("="*50 + "\n")
    
    # Run tests
    conn_ok = test_connection()
    service_ok = test_services()
    
    print("\n" + "="*50)
    if conn_ok and service_ok:
        print("✅ ALL TESTS PASSED - Ready to run the app!")
        print("="*50)
        sys.exit(0)
    else:
        print("❌ TESTS FAILED - Please fix issues before running the app")
        print("="*50)
        sys.exit(1)
