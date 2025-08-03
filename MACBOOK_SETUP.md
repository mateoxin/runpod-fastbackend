# 🍎 MacBook Setup Guide for FastBackend Tests

## ✅ Installation Complete!

All necessary libraries have been installed on your MacBook to run the FastBackend tests.

## 📦 What's Installed

- **Python 3.9.6** (system version)
- **Virtual Environment** (`venv/`) with isolated dependencies
- **Core Dependencies:**
  - `runpod>=1.7.0` - RunPod API client
  - `fastapi>=0.104.0` - Web framework for testing
  - `uvicorn>=0.24.0` - ASGI server
  - `pyyaml>=6.0` - YAML configuration
  - `Pillow>=10.0.0` - Image processing
  - `python-dotenv>=1.0.0` - Environment variables
  - `requests>=2.31.0` - HTTP requests
- **Testing Dependencies:**
  - `pytest>=8.4.1` - Testing framework
  - `pytest-asyncio>=1.1.0` - Async testing support

## 🚀 How to Run Tests

### Option 1: Use the Convenience Script (Recommended)
```bash
# Quick basic test
./activate_and_test.sh simple

# Full test suite
./activate_and_test.sh all

# Run with pytest
./activate_and_test.sh pytest

# Quick deployment test
./activate_and_test.sh quick

# Local testing
./activate_and_test.sh local
```

### Option 2: Manual Commands
```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python tests/simple_test.py
python tests/run_all_tests.py
python -m pytest tests/

# Deactivate when done
deactivate
```

## 🧪 Test Results Summary

✅ **Basic functionality test**: PASSED  
✅ **Handler methods test**: PASSED (22/22 tests)  
⚠️ **Deployment methods test**: PARTIAL (15/18 tests passed)  
⚠️ **Local testing test**: PARTIAL (12/18 tests passed)  

*Note: Some tests fail because they require API keys or external services, which is expected for local testing.*

## 📁 Project Structure

```
runpod-fastbackend/
├── venv/                    # Virtual environment (created)
├── tests/                   # Test files
│   ├── simple_test.py      # Quick basic test
│   ├── run_all_tests.py    # Full test suite
│   └── ...                 # Other test files
├── activate_and_test.sh    # Convenience script (created)
├── requirements.txt        # Dependencies
└── handler_fast.py         # Main handler
```

## 🔧 Troubleshooting

### If you get "command not found: python"
```bash
# Use python3 instead
python3 tests/simple_test.py
```

### If virtual environment is not activated
```bash
source venv/bin/activate
```

### If you need to reinstall dependencies
```bash
# Remove and recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-asyncio
```

### If tests fail with import errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
# Check if packages are installed
pip list | grep runpod
```

## 🎯 Next Steps

1. **Run a quick test**: `./activate_and_test.sh simple`
2. **Explore the codebase**: Check `handler_fast.py` and test files
3. **Add your own tests**: Create new test files in the `tests/` directory
4. **Set up API keys**: For deployment tests, you'll need RunPod API keys

## 📞 Support

If you encounter any issues:
1. Check that the virtual environment is activated
2. Verify all dependencies are installed: `pip list`
3. Try running the simple test first: `./activate_and_test.sh simple`

---

**🎉 You're all set! Your MacBook is ready to run FastBackend tests.** 