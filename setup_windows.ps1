Write-Host "🎓 Setting up Mini LMS..."

# Check if python is available
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not installed or not in PATH."
    exit 1
}

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..."
    python -m venv venv
}

# Install dependencies from requirements.txt
Write-Host "📦 Installing dependencies..."
.\venv\Scripts\python.exe -m pip install -r requirements.txt

# Run migrations
Write-Host "🗃️ Running migrations..."
.\venv\Scripts\python.exe backend\manage.py makemigrations accounts
.\venv\Scripts\python.exe backend\manage.py makemigrations courses
.\venv\Scripts\python.exe backend\manage.py migrate

# Create demo data
Write-Host "👤 Creating demo users and data..."
# Use backend path for create_demo_data.py
.\venv\Scripts\python.exe backend\create_demo_data.py

# Start server
Write-Host "🚀 Starting server..."
Write-Host "   Open: http://localhost:8000"
.\venv\Scripts\python.exe backend\manage.py runserver
