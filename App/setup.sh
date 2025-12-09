
#!/bin/bash
# Setup script for Modern Manager

APP_DIR=$(dirname "$0")
cd "$APP_DIR"

# 1. Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate venv
echo "📦 Activating virtual environment..."
source venv/bin/activate

# 3. Upgrade pip and install requirements
echo "⬆️  Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run the app
echo "🚀 Starting Modern Manager..."
python src/main.py
