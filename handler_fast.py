#!/usr/bin/env python3
"""
🧪 SIMPLE TEST HANDLER - dla testów RunPod
Zastępuje skomplikowany handler prostym do diagnozy
"""

import runpod
import json
import sys
from datetime import datetime

def handler(job):
    """Prosty handler do testowania"""
    print(f"🎯 [SIMPLE] Received job: {job}")
    
    try:
        job_input = job.get("input", {})
        job_type = job_input.get("type", "test")
        
        print(f"📦 [SIMPLE] Processing: {job_type}")
        
        # Podstawowe odpowiedzi
        if job_type == "health":
            result = {
                "status": "healthy",
                "message": "Simple handler working!",
                "timestamp": datetime.now().isoformat(),
                "version": "simple-test-1.0"
            }
        elif job_type == "echo":
            result = {
                "status": "success", 
                "echo": job_input,
                "timestamp": datetime.now().isoformat()
            }
        elif job_type == "ping":
            result = {
                "status": "pong",
                "message": "Simple handler responding!",
                "timestamp": datetime.now().isoformat()
            }
        else:
            result = {
                "status": "success",
                "message": f"Processed {job_type}",
                "received_input": job_input,
                "timestamp": datetime.now().isoformat(),
                "note": "Simple test handler - no heavy processing"
            }
        
        print(f"✅ [SIMPLE] Returning: {json.dumps(result, indent=2)}")
        return result
        
    except Exception as e:
        error_result = {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "handler_type": "simple"
        }
        print(f"❌ [SIMPLE] Error: {json.dumps(error_result, indent=2)}")
        return error_result

if __name__ == "__main__":
    print("🚀 [SIMPLE] Starting simple test handler...")
    print("=" * 50)
    print("✨ Features:")
    print("  - No heavy dependencies")
    print("  - Instant responses")
    print("  - Simple logging")
    print("  - Basic job processing")
    print("=" * 50)
    
    # Test lokalny
    if "--test_input" in sys.argv:
        try:
            test_input_index = sys.argv.index("--test_input") + 1
            if test_input_index < len(sys.argv):
                test_input_str = sys.argv[test_input_index]
                test_job = json.loads(test_input_str)
                
                print("🧪 [TEST] Running local test...")
                result = handler(test_job)
                print(f"🧪 [TEST] Result: {json.dumps(result, indent=2)}")
                sys.exit(0)
        except (ValueError, json.JSONDecodeError) as e:
            print(f"❌ [TEST] Invalid test input: {e}")
            sys.exit(1)
    
    # RunPod serverless
    print("🔗 [RUNPOD] Starting serverless worker...")
    runpod.serverless.start({"handler": handler})