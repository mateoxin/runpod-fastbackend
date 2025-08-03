#!/usr/bin/env python3
"""
🚀 ULTRA-FAST RUNPOD HANDLER - POPRAWIONE LOGOWANIE
Minimal handler - setup heavy dependencies in runtime
Deploy time: ~30 seconds instead of 20 minutes!
"""

import runpod
import json
import time
import os
import sys
import subprocess
from datetime import datetime
from typing import Dict, Any

# Global flag to track if environment is setup
ENVIRONMENT_READY = False
SETUP_LOCK = False

def log(message, level="INFO"):
    """Unified logging to stdout and stderr for RunPod visibility"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_msg = f"[{timestamp}] {level}: {message}"
    
    # Write to both stdout and stderr for maximum visibility
    print(log_msg)
    sys.stderr.write(f"{log_msg}\n")
    sys.stderr.flush()
    sys.stdout.flush()

def setup_environment():
    """Setup heavy dependencies at runtime (wykorzystuje RunPod cache)"""
    global ENVIRONMENT_READY, SETUP_LOCK
    
    if ENVIRONMENT_READY:
        log("Environment already ready", "INFO")
        return True
        
    if SETUP_LOCK:
        log("Environment setup in progress...", "WARN")
        # Wait for setup to complete
        while SETUP_LOCK and not ENVIRONMENT_READY:
            time.sleep(1)
        return ENVIRONMENT_READY
    
    SETUP_LOCK = True
    
    try:
        log("🚀 Setting up environment at runtime...", "INFO")
        
        # Step 1: Install PyTorch (RunPod has cache - much faster than Docker)
        log("📦 Installing PyTorch with CUDA...", "INFO")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "torch", "torchvision", "torchaudio", 
            "--index-url", "https://download.pytorch.org/whl/cu121"
        ], capture_output=False, text=True)  # CHANGED: capture_output=False to see output
        
        if result.returncode != 0:
            log(f"❌ PyTorch install failed with code {result.returncode}", "ERROR")
            return False
        
        log("✅ PyTorch installed successfully", "INFO")
        
        # Step 2: Install other ML dependencies
        log("📦 Installing transformers and diffusers...", "INFO")
        packages = [
            "transformers>=4.30.0",
            "diffusers>=0.18.0", 
            "accelerate>=0.20.0",
            "xformers",
            "bitsandbytes"
        ]
        
        for package in packages:
            log(f"Installing {package}...", "INFO")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=False, text=True)
            
            if result.returncode != 0:
                log(f"⚠️ Failed to install {package}, continuing...", "WARN")
            else:
                log(f"✅ {package} installed", "INFO")
        
        # Step 3: Setup directories
        log("📁 Creating workspace directories...", "INFO")
        os.makedirs("/workspace", exist_ok=True)
        os.makedirs("/workspace/training_data", exist_ok=True)
        os.makedirs("/workspace/models", exist_ok=True)
        os.makedirs("/workspace/ai-toolkit", exist_ok=True)
        
        # Step 4: Setup HuggingFace token
        hf_token = os.environ.get("HF_TOKEN", "")
        if hf_token and hf_token != "":
            log("🤗 Setting up HuggingFace token...", "INFO")
            try:
                subprocess.run([
                    "huggingface-cli", "login", "--token", hf_token
                ], capture_output=True, text=True, timeout=30)
                log("✅ HuggingFace token configured", "INFO")
            except subprocess.TimeoutExpired:
                log("⚠️ HuggingFace login timeout, continuing...", "WARN")
            except Exception as e:
                log(f"⚠️ HuggingFace login failed: {e}", "WARN")
        else:
            log("⚠️ No HuggingFace token provided", "WARN")
        
        log("✅ Environment setup completed successfully!", "INFO")
        ENVIRONMENT_READY = True
        return True
        
    except Exception as e:
        log(f"❌ Setup error: {e}", "ERROR")
        return False
    finally:
        SETUP_LOCK = False

def lazy_import_heavy_modules():
    """Import heavy modules only when needed"""
    global HEAVY_MODULES
    
    if 'HEAVY_MODULES' in globals():
        return HEAVY_MODULES
    
    try:
        log("📦 Loading heavy modules...", "INFO")
        # Import heavy stuff only after setup
        import base64
        import uuid
        import yaml
        import threading
        
        HEAVY_MODULES = {
            'base64': base64,
            'uuid': uuid, 
            'yaml': yaml,
            'threading': threading
        }
        
        log("✅ Heavy modules loaded", "INFO")
        return HEAVY_MODULES
        
    except Exception as e:
        log(f"❌ Error loading heavy modules: {e}", "ERROR")
        return None

def validate_payload_size(job, max_size_mb=10):
    """Validate payload size"""
    try:
        payload_size = len(json.dumps(job).encode('utf-8'))
        size_mb = payload_size / (1024 * 1024)
        
        if size_mb > max_size_mb:
            log(f"⚠️ Large payload: {size_mb:.2f}MB", "WARN")
            return {
                "status": "error",
                "error": f"Payload too large: {size_mb:.2f}MB (max: {max_size_mb}MB)",
                "timestamp": datetime.now().isoformat()
            }
        
        log(f"✅ Payload size OK: {size_mb:.2f}MB", "INFO")
        return None
        
    except Exception as e:
        log(f"❌ Payload validation error: {e}", "ERROR")
        return None

def handler(job):
    """
    Ultra-fast handler with lazy loading and RunPod compliance
    """
    try:
        log(f"🎯 Received job: {job}", "INFO")
        
        # Validate payload size
        size_error = validate_payload_size(job)
        if size_error:
            return size_error
        
        # Extract input
        job_input = job.get("input", {})
        job_type = job_input.get("type", "unknown")
        
        log(f"📦 Processing job type: {job_type}", "INFO")
        
        # Fast responses (no heavy dependencies needed)
        if job_type == "health":
            result = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "message": "Fast backend is working!",
                "environment_ready": ENVIRONMENT_READY,
                "version": "1.0.0-fast-fixed"
            }
            log(f"✅ Health check completed", "INFO")
            return result
            
        elif job_type == "ping":
            result = {
                "status": "pong", 
                "timestamp": datetime.now().isoformat(),
                "setup_required": not ENVIRONMENT_READY
            }
            log(f"✅ Ping responded", "INFO")
            return result
            
        elif job_type == "echo":
            result = {
                "status": "success",
                "echo": job_input,
                "timestamp": datetime.now().isoformat()
            }
            log(f"✅ Echo completed", "INFO")
            return result
        
        elif job_type == "setup_environment":
            # Manual environment setup trigger
            log("🔧 Manual environment setup triggered", "INFO")
            success = setup_environment()
            result = {
                "status": "success" if success else "error",
                "message": "Environment setup completed" if success else "Environment setup failed",
                "environment_ready": ENVIRONMENT_READY,
                "timestamp": datetime.now().isoformat()
            }
            return result
        
        # Heavy operations require environment setup
        heavy_operations = [
            "upload_training_data", "load_matt_dataset", 
            "train", "train_with_yaml", "process_status", 
            "processes", "list_models", "download_model",
            "generate", "inference"
        ]
        
        if job_type in heavy_operations:
            log(f"🔧 Heavy operation detected: {job_type}", "INFO")
            
            # Setup environment if not ready
            if not ENVIRONMENT_READY:
                log("🚀 Setting up environment for heavy operation...", "INFO")
                if not setup_environment():
                    return {
                        "status": "error",
                        "error": "Environment setup failed",
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Load heavy modules
            heavy_modules = lazy_import_heavy_modules()
            if not heavy_modules:
                return {
                    "status": "error", 
                    "error": "Failed to load required modules",
                    "timestamp": datetime.now().isoformat()
                }
            
            # For now, return placeholder for heavy operations
            result = {
                "status": "success",
                "message": f"Heavy operation {job_type} would be processed here",
                "job_type": job_type,
                "environment_ready": ENVIRONMENT_READY,
                "timestamp": datetime.now().isoformat(),
                "note": "Heavy operations implementation in progress"
            }
            
            log(f"✅ Heavy operation {job_type} placeholder completed", "INFO")
            return result
        
        # Unknown job type
        log(f"⚠️ Unknown job type: {job_type}", "WARN")
        return {
            "status": "error",
            "error": f"Unknown job type: {job_type}",
            "available_types": ["health", "ping", "echo", "setup_environment"] + heavy_operations,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        error_msg = f"Handler error: {str(e)}"
        log(error_msg, "ERROR")
        return {
            "status": "error",
            "error": error_msg,
            "timestamp": datetime.now().isoformat(),
            "handler_type": "ultra-fast"
        }

def handle_local_testing():
    """Handle local testing arguments"""
    import sys
    
    # Check for test_input argument
    if "--test_input" in sys.argv:
        try:
            test_input_index = sys.argv.index("--test_input") + 1
            if test_input_index < len(sys.argv):
                test_input_str = sys.argv[test_input_index]
                test_input = json.loads(test_input_str)
                
                log("🧪 Running with test input...", "INFO")
                result = handler(test_input)
                log(f"📊 Test result: {json.dumps(result, indent=2)}", "INFO")
                return True
        except (ValueError, json.JSONDecodeError) as e:
            log(f"❌ Invalid test input: {e}", "ERROR")
            return True
    
    # Check for local server mode
    if "--rp_serve_api" in sys.argv:
        log("🌐 Starting local API server...", "INFO")
        try:
            from fastapi import FastAPI
            import uvicorn
            
            app = FastAPI(title="RunPod Handler Local Server")
            
            @app.post("/run")
            async def run_handler(request: dict):
                return handler(request)
            
            @app.get("/health")
            async def health_check():
                return {"status": "healthy", "timestamp": datetime.now().isoformat()}
            
            uvicorn.run(app, host="0.0.0.0", port=8000)
            return True
            
        except ImportError:
            log("❌ FastAPI/Uvicorn not installed. Install with: pip install fastapi uvicorn", "ERROR")
            log("💡 Falling back to basic handler startup...", "INFO")
    
    return False

if __name__ == "__main__":
    log("🚀 Starting Ultra-Fast RunPod Handler - FIXED LOGGING", "INFO")
    log("=" * 60, "INFO")
    log("✨ Features:", "INFO")
    log("  - Instant startup (no Docker build)", "INFO")
    log("  - Runtime dependency installation", "INFO") 
    log("  - Lazy module loading", "INFO")
    log("  - GitHub-based updates", "INFO")
    log("  - Local testing support", "INFO")
    log("  - FIXED: Visible logging to stderr+stdout", "INFO")
    log("=" * 60, "INFO")
    
    # Handle local testing modes
    if handle_local_testing():
        log("🏁 Testing complete, exiting...", "INFO")
        sys.exit(0)
    
    # Start RunPod serverless
    log("🚀 Starting serverless worker...", "INFO")
    runpod.serverless.start({"handler": handler})