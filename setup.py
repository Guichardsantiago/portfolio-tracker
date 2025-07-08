#!/usr/bin/env python3
"""
Setup script for the Portfolio Tracker API.
This script automates the initial setup process.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Portfolio Tracker API")
    print("=" * 50)
    
    # Check if Python is available
    if not run_command("python --version", "Checking Python installation"):
        print("❌ Python is not available. Please install Python 3.8+ and try again.")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your pip installation.")
        sys.exit(1)
    
    # Create migrations
    if not run_command("python manage.py makemigrations portfolio", "Creating database migrations"):
        print("❌ Failed to create migrations.")
        sys.exit(1)
    
    # Apply migrations
    if not run_command("python manage.py migrate", "Applying database migrations"):
        print("❌ Failed to apply migrations.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print("\n2. (Optional) Create a superuser for admin access:")
    print("   python manage.py createsuperuser")
    print("\n3. Test the API:")
    print("   python test_api.py")
    print("\n4. Access the admin interface at: http://localhost:8000/admin/")
    print("5. API endpoints available at: http://localhost:8000/api/")

if __name__ == "__main__":
    main() 