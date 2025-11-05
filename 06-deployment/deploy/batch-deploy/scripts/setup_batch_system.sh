#!/bin/bash

# NYC Taxi Batch Prediction System Setup Script
# This script sets up the complete batch prediction environment

set -e  # Exit on any error

echo "🚀 Setting up NYC Taxi Batch Prediction System"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [[ ! -f "pyproject.toml" ]]; then
    print_error "pyproject.toml not found. Please run this script from the batch-deploy directory."
    exit 1
fi

print_status "Checking prerequisites..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_success "Python $PYTHON_VERSION found"

# Check UV
if ! command -v uv &> /dev/null; then
    print_error "UV is required but not installed. Please install UV first."
    print_status "Install UV with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

UV_VERSION=$(uv --version | cut -d' ' -f2)
print_success "UV $UV_VERSION found"

# Check if model file exists
if [[ ! -f "lin_reg.bin" ]]; then
    print_error "Model file 'lin_reg.bin' not found."
    print_status "Please copy the model file from the web-service directory:"
    print_status "cp ../web-service/lin_reg.bin ."
    exit 1
fi

print_success "Model file found"

# Install dependencies
print_status "Installing dependencies with UV..."
if uv sync; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Create necessary directories
print_status "Creating directory structure..."
mkdir -p data/{input,output,processed} logs config

# Set up environment file
print_status "Creating environment configuration..."
cat > .env << EOF
# NYC Taxi Batch Prediction Environment Configuration
LOG_LEVEL=INFO
BATCH_SIZE=1000
MAX_WORKERS=4
NUM_TRIPS_PER_BATCH=5000

# Prefect Configuration
PREFECT_API_URL=
PREFECT_WORK_POOL=default-agent-pool

# Scheduling (cron format)
BATCH_SCHEDULE_CRON=0 */2 * * *
CLEANUP_SCHEDULE_CRON=0 2 * * *

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=8000

# Retention (days)
OUTPUT_RETENTION_DAYS=30
LOG_RETENTION_DAYS=7
EOF

print_success "Environment file created"

# Test the system
print_status "Testing the batch prediction system..."

# Generate sample data
print_status "Generating sample data..."
if uv run python src/data_generator.py; then
    print_success "Sample data generated"
else
    print_warning "Sample data generation failed (non-critical)"
fi

# Check Prefect server status
print_status "Checking Prefect server..."
if uv run prefect server start --host 0.0.0.0 --port 4200 &
then
    PREFECT_PID=$!
    sleep 5
    
    if kill -0 $PREFECT_PID 2>/dev/null; then
        print_success "Prefect server started successfully (PID: $PREFECT_PID)"
        print_status "Stopping test server..."
        kill $PREFECT_PID
        wait $PREFECT_PID 2>/dev/null || true
    else
        print_warning "Prefect server test failed (non-critical)"
    fi
else
    print_warning "Could not start Prefect server (non-critical)"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
echo "📋 Next Steps:"
echo "1. Start Prefect server:"
echo "   uv run prefect server start --host 0.0.0.0 --port 4200"
echo ""
echo "2. In another terminal, create deployments:"
echo "   uv run python scripts/deploy_prefect.py"
echo ""
echo "3. Start a worker:"
echo "   uv run prefect worker start --pool default-agent-pool"
echo ""
echo "4. Or run flows locally for development:"
echo "   uv run python scripts/deploy_prefect.py serve"
echo ""
echo "📊 Test the system:"
echo "   uv run python src/data_generator.py"
echo "   uv run python src/batch_predictor.py"
echo ""
echo "🌐 Access Prefect UI at: http://localhost:4200"
echo ""
echo "📁 Directory structure:"
echo "   data/input/     - Input batch files"
echo "   data/output/    - Prediction results"
echo "   data/processed/ - Processed input files"
echo "   logs/           - Application logs"
echo ""
print_success "System is ready for batch predictions! 🚀"
