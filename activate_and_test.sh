#!/bin/bash

echo "🚀 FastBackend Test Environment Setup"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run the installation first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if we're in the virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"

# Show available test options
echo ""
echo "🧪 Available test commands:"
echo "1. python tests/simple_test.py          - Quick basic test"
echo "2. python tests/run_all_tests.py        - Full test suite"
echo "3. python -m pytest tests/              - Run with pytest"
echo "4. python quick_test.py                 - Quick deployment test"
echo "5. python test_local.py                 - Local testing"

echo ""
echo "💡 To run tests manually, first activate the environment:"
echo "   source venv/bin/activate"
echo ""
echo "💡 To deactivate the environment:"
echo "   deactivate"
echo ""

# Check if any arguments were passed
if [ $# -eq 0 ]; then
    echo "🎯 No test specified. Run a test manually or use one of the commands above."
    echo "   Example: ./activate_and_test.sh simple"
    exit 0
fi

# Run specific test based on argument
case $1 in
    "simple")
        echo "🧪 Running simple test..."
        python tests/simple_test.py
        ;;
    "all")
        echo "🧪 Running all tests..."
        python tests/run_all_tests.py
        ;;
    "pytest")
        echo "🧪 Running pytest..."
        python -m pytest tests/
        ;;
    "quick")
        echo "🧪 Running quick test..."
        python quick_test.py
        ;;
    "local")
        echo "🧪 Running local test..."
        python test_local.py
        ;;
    *)
        echo "❌ Unknown test type: $1"
        echo "Available options: simple, all, pytest, quick, local"
        exit 1
        ;;
esac 