#!/usr/bin/env python3
"""
🧪 Testy dla RTX 5090 Endpoint
Testuje nowy endpoint z najnowszą kartą RTX 5090 (32GB VRAM)
"""

import sys
import os
import json
import unittest
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import runpod for endpoint testing
try:
    import runpod
    from dotenv import load_dotenv
    RUNPOD_AVAILABLE = True
except ImportError:
    RUNPOD_AVAILABLE = False
    print("⚠️  RunPod not available - install with: pip install runpod python-dotenv")

class TestRTX5090Endpoint(unittest.TestCase):
    """Testy dla RTX 5090 endpoint"""
    
    @classmethod
    def setUpClass(cls):
        """Setup endpoint info"""
        if not RUNPOD_AVAILABLE:
            cls.skipTest(cls, "RunPod not available")
            return
            
        # Load endpoint info
        try:
            with open('../endpoint_working_info.json', 'r') as f:
                cls.endpoint_info = json.load(f)
        except FileNotFoundError:
            cls.skipTest(cls, "endpoint_working_info.json not found")
            return
        
        # Setup RunPod API
        load_dotenv('../config.env')
        runpod.api_key = os.getenv('RUNPOD_API_KEY')
        
        if not runpod.api_key:
            cls.skipTest(cls, "RUNPOD_API_KEY not set")
            return
        
        cls.endpoint_id = cls.endpoint_info['id']
        cls.endpoint = runpod.Endpoint(cls.endpoint_id)
        
        print(f"🚀 Testing RTX 5090 Endpoint: {cls.endpoint_id}")
        print(f"🖥️  GPU: {cls.endpoint_info['gpu_name']} ({cls.endpoint_info['gpu_memory']})")
    
    def test_01_endpoint_health(self):
        """Test 1: Basic health check"""
        print("\n🧪 Test 1: RTX 5090 Health Check")
        
        payload = {
            "input": {
                "type": "health",
                "message": "RTX 5090 endpoint test",
                "gpu_target": "RTX 5090",
                "memory_target": "32GB"
            }
        }
        
        start_time = time.time()
        result = self.endpoint.run_sync(payload, timeout=120)
        response_time = time.time() - start_time
        
        self.assertIsNotNone(result, "Health check should return result")
        print(f"✅ Health check completed in {response_time:.1f}s")
        print(f"📋 Response: {json.dumps(result, indent=2)}")
    
    def test_02_performance_ping(self):
        """Test 2: Performance ping"""
        print("\n🧪 Test 2: RTX 5090 Performance Ping")
        
        payload = {
            "input": {
                "type": "ping"
            }
        }
        
        start_time = time.time()
        result = self.endpoint.run_sync(payload, timeout=60)
        response_time = time.time() - start_time
        
        self.assertIsNotNone(result, "Ping should return result")
        print(f"✅ Ping completed in {response_time:.1f}s")
        
        # Check if response time is reasonable (active worker should be fast)
        if response_time < 10:
            print("🚀 EXCELLENT response time - active worker working!")
        elif response_time < 30:
            print("✅ Good response time")
        else:
            print("⚠️  Slow response - may be cold start")
    
    def test_03_echo_with_gpu_data(self):
        """Test 3: Echo test with GPU data"""
        print("\n🧪 Test 3: Echo with RTX 5090 Data")
        
        test_data = {
            "endpoint_version": "working",
            "gpu_type": "RTX 5090",
            "gpu_memory": "32GB",
            "active_worker": True,
            "test_timestamp": datetime.now().isoformat(),
            "large_data": "x" * 1000  # Test with some data
        }
        
        payload = {
            "input": {
                "type": "echo",
                "test_data": test_data
            }
        }
        
        start_time = time.time()
        result = self.endpoint.run_sync(payload, timeout=90)
        response_time = time.time() - start_time
        
        self.assertIsNotNone(result, "Echo should return result")
        print(f"✅ Echo completed in {response_time:.1f}s")
        
        # Verify echo returned our data
        if isinstance(result, dict) and 'echo' in result:
            echo_data = result['echo']
            self.assertEqual(echo_data.get('test_data', {}).get('gpu_type'), 'RTX 5090')
            print("✅ Echo data verification passed")
    
    def test_04_environment_setup(self):
        """Test 4: Heavy environment setup"""
        print("\n🧪 Test 4: Environment Setup on RTX 5090")
        
        payload = {
            "input": {
                "type": "setup_environment"
            }
        }
        
        print("📤 Starting environment setup (may take 2-5 minutes)...")
        start_time = time.time()
        result = self.endpoint.run_sync(payload, timeout=600)  # 10 min timeout
        response_time = time.time() - start_time
        
        self.assertIsNotNone(result, "Environment setup should return result")
        print(f"✅ Environment setup completed in {response_time:.1f}s")
        print(f"🔧 Setup result: {json.dumps(result, indent=2)}")
        
        # Check if environment is ready
        if isinstance(result, dict):
            status = result.get('status', 'unknown')
            if status == 'success':
                print("🎉 Environment setup SUCCESSFUL")
            else:
                print(f"⚠️  Environment setup status: {status}")
    
    def test_05_performance_benchmark(self):
        """Test 5: Performance benchmark"""
        print("\n🧪 Test 5: RTX 5090 Performance Benchmark")
        
        ping_times = []
        
        for i in range(5):
            payload = {"input": {"type": "ping"}}
            
            start_time = time.time()
            result = self.endpoint.run_sync(payload, timeout=30)
            end_time = time.time()
            
            if result:
                ping_time = end_time - start_time
                ping_times.append(ping_time)
                print(f"🏓 Ping {i+1}: {ping_time:.2f}s")
            else:
                print(f"❌ Ping {i+1}: FAILED")
        
        self.assertGreater(len(ping_times), 0, "At least one ping should succeed")
        
        if ping_times:
            avg_ping = sum(ping_times) / len(ping_times)
            min_ping = min(ping_times)
            max_ping = max(ping_times)
            
            print(f"\n📊 RTX 5090 Benchmark Results:")
            print(f"   ⚡ Average response: {avg_ping:.2f}s")
            print(f"   🚀 Fastest response: {min_ping:.2f}s")
            print(f"   🐌 Slowest response: {max_ping:.2f}s")
            
            # Performance assertions
            self.assertLess(avg_ping, 60, "Average ping should be under 60s")
            self.assertLess(min_ping, 30, "Fastest ping should be under 30s")
    
    def test_06_list_models(self):
        """Test 6: List available models"""
        print("\n🧪 Test 6: List Models on RTX 5090")
        
        payload = {
            "input": {
                "type": "list_models"
            }
        }
        
        start_time = time.time()
        result = self.endpoint.run_sync(payload, timeout=120)
        response_time = time.time() - start_time
        
        self.assertIsNotNone(result, "List models should return result")
        print(f"✅ Models listing completed in {response_time:.1f}s")
        print(f"📁 Models result: {json.dumps(result, indent=2)}")

def run_rtx5090_tests():
    """Run RTX 5090 endpoint tests"""
    print("🚀 RTX 5090 Endpoint Test Suite")
    print("=" * 50)
    
    # Load test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestRTX5090Endpoint)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RTX 5090 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 All RTX 5090 tests PASSED!")
        return True
    else:
        print("\n⚠️  Some RTX 5090 tests FAILED")
        return False

if __name__ == "__main__":
    if not RUNPOD_AVAILABLE:
        print("❌ RunPod not available")
        sys.exit(1)
    
    success = run_rtx5090_tests()
    sys.exit(0 if success else 1)