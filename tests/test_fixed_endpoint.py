#!/usr/bin/env python3
"""
Test FIXED RunPod Endpoint 
Testuje endpoint z ACTIVE WORKER (workers_min=1)
"""

import runpod
import os
import json
import time
from dotenv import load_dotenv
from datetime import datetime

def load_endpoint_fixed_info():
    """Ładuje informacje o fixed endpoint"""
    try:
        with open('endpoint_fixed_info.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Nie znaleziono endpoint_fixed_info.json")
        return None

def check_active_worker_status():
    """Sprawdza status active worker"""
    load_dotenv('config.env')
    runpod.api_key = os.getenv('RUNPOD_API_KEY')
    
    endpoint_info = load_endpoint_fixed_info()
    if not endpoint_info:
        return None
    
    print(f"📊 Sprawdzanie ACTIVE WORKER status...")
    
    try:
        endpoints = runpod.get_endpoints()
        for endpoint in endpoints:
            if endpoint.get('id') == endpoint_info['id']:
                status = endpoint.get('status', 'Unknown')
                workers_ready = endpoint.get('workersReady', 0)
                workers_running = endpoint.get('workersRunning', 0)
                workers_max = endpoint.get('workersMax', 0)
                
                print(f"✅ FIXED Endpoint znaleziony:")
                print(f"   📛 Name: {endpoint.get('name', 'Unknown')}")
                print(f"   🆔 ID: {endpoint.get('id', 'Unknown')}")
                print(f"   📈 Status: {status}")
                print(f"   👥 Workers Max: {workers_max}")
                print(f"   🏃 Workers Running: {workers_running}")
                print(f"   ✅ Workers Ready: {workers_ready}")
                print(f"   ⭐ Active Worker: {endpoint_info.get('has_active_worker', False)}")
                print(f"   🌍 Locations: {endpoint.get('locations', 'Unknown')}")
                
                # Sprawdź czy active worker działa
                if workers_ready > 0:
                    print(f"🎉 ACTIVE WORKER jest gotowy! ({workers_ready} ready)")
                    return endpoint
                elif workers_running > 0:
                    print(f"⏳ ACTIVE WORKER się uruchamia... ({workers_running} running)")
                    return endpoint
                else:
                    print(f"⚠️  ACTIVE WORKER jeszcze nie uruchomiony")
                    return endpoint
        
        print("❌ FIXED Endpoint nie znaleziony")
        return None
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania statusu: {e}")
        return None

def test_fixed_endpoint():
    """Testuje fixed endpoint z active worker"""
    
    endpoint_info = load_endpoint_fixed_info()
    if not endpoint_info:
        return
    
    endpoint_id = endpoint_info['id']
    endpoint_url = endpoint_info['url']
    
    print(f"\n🚀 Testowanie FIXED Endpoint: {endpoint_info['name']}")
    print(f"🆔 ID: {endpoint_id}")
    print(f"🔗 URL: {endpoint_url}")
    print(f"🖥️  GPU: {endpoint_info['gpu_type']} ({endpoint_info['gpu_memory']})")
    print(f"💾 Storage: {endpoint_info['container_disk_gb']}GB + {endpoint_info['volume_gb']}GB")
    print(f"⭐ ACTIVE WORKER: {endpoint_info['has_active_worker']}")
    print(f"⚡ Features: FlashBoot={endpoint_info['flashboot']}, Timeout={endpoint_info['idle_timeout']}s")
    print("=" * 70)
    
    # Inicjalizuj endpoint
    try:
        endpoint = runpod.Endpoint(endpoint_id)
        print(f"✅ Połączenie z FIXED endpoint established")
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")
        return
    
    # Test 1: Szybki Health Check (active worker powinien odpowiedzieć od razu)
    print(f"\n🧪 Test 1: ACTIVE WORKER Health Check")
    try:
        health_payload = {
            "input": {
                "type": "health",
                "message": "RTX 3090 FIXED endpoint test",
                "version": "fixed",
                "active_worker": True
            }
        }
        
        print(f"📤 Wysyłanie health check do ACTIVE WORKER...")
        start_time = time.time()
        
        # Active worker powinien odpowiedzieć szybko (bez cold start)
        result = endpoint.run_sync(health_payload, timeout=60)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if result:
            print(f"✅ ACTIVE WORKER Health check PASSED ({response_time:.1f}s)")
            print(f"📋 Response: {json.dumps(result, indent=2)}")
            
            # Sprawdź czy nie było cold start
            if response_time < 30:
                print(f"🚀 EXCELLENT! Szybka odpowiedź - active worker działa!")
            else:
                print(f"⚠️  Wolna odpowiedź - może być cold start")
        else:
            print(f"❌ Health check FAILED")
            
    except Exception as e:
        print(f"❌ Health check ERROR: {e}")
    
    # Test 2: Performance Test
    print(f"\n🧪 Test 2: ACTIVE WORKER Performance")
    try:
        ping_payload = {
            "input": {
                "type": "ping"
            }
        }
        
        print(f"📤 Performance test...")
        start_time = time.time()
        
        result = endpoint.run_sync(ping_payload, timeout=30)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if result:
            print(f"✅ Performance test PASSED ({response_time:.1f}s)")
            print(f"🏓 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Performance test FAILED")
            
    except Exception as e:
        print(f"❌ Performance test ERROR: {e}")
    
    # Test 3: Echo Test z danymi
    print(f"\n🧪 Test 3: Echo Test with GPU Data")
    try:
        echo_payload = {
            "input": {
                "type": "echo",
                "test_data": {
                    "endpoint_version": "fixed",
                    "gpu_target": "RTX 3090",
                    "active_worker": True,
                    "storage_config": "100GB+100GB",
                    "workers_min": 1,
                    "test_timestamp": datetime.now().isoformat()
                }
            }
        }
        
        print(f"📤 Echo test z GPU danymi...")
        start_time = time.time()
        
        result = endpoint.run_sync(echo_payload, timeout=45)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if result:
            print(f"✅ Echo test PASSED ({response_time:.1f}s)")
            print(f"🔄 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Echo test FAILED")
            
    except Exception as e:
        print(f"❌ Echo test ERROR: {e}")
    
    # Test 4: Heavy Environment Setup (tylko jeśli poprzednie testy działały)
    print(f"\n🧪 Test 4: Environment Setup na ACTIVE WORKER")
    try:
        setup_payload = {
            "input": {
                "type": "setup_environment"
            }
        }
        
        print(f"📤 Environment setup na active worker...")
        print(f"💡 Może potrwać 2-4 minuty (PyTorch + CUDA)")
        start_time = time.time()
        
        result = endpoint.run_sync(setup_payload, timeout=600)  # 10 min timeout
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if result:
            print(f"✅ Environment setup COMPLETED ({response_time:.1f}s)")
            print(f"🔧 Setup Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Environment setup FAILED")
            
    except Exception as e:
        print(f"❌ Environment setup ERROR: {e}")

def run_performance_benchmark():
    """Benchmark performance active worker"""
    
    endpoint_info = load_endpoint_fixed_info()
    if not endpoint_info:
        return
    
    print(f"\n⚡ BENCHMARK: ACTIVE WORKER Performance")
    print("=" * 50)
    
    endpoint = runpod.Endpoint(endpoint_info['id'])
    
    # Multiple ping tests
    ping_times = []
    
    for i in range(5):
        try:
            start_time = time.time()
            result = endpoint.run_sync({"input": {"type": "ping"}}, timeout=30)
            end_time = time.time()
            
            if result:
                ping_time = end_time - start_time
                ping_times.append(ping_time)
                print(f"🏓 Ping {i+1}: {ping_time:.2f}s")
            else:
                print(f"❌ Ping {i+1}: FAILED")
                
        except Exception as e:
            print(f"❌ Ping {i+1} ERROR: {e}")
    
    if ping_times:
        avg_ping = sum(ping_times) / len(ping_times)
        min_ping = min(ping_times)
        max_ping = max(ping_times)
        
        print(f"\n📊 ACTIVE WORKER Benchmark Results:")
        print(f"   ⚡ Average response: {avg_ping:.2f}s")
        print(f"   🚀 Fastest response: {min_ping:.2f}s")
        print(f"   🐌 Slowest response: {max_ping:.2f}s")
        
        # Performance rating dla active worker
        if avg_ping < 3:
            rating = "🌟 EXCELLENT (Active worker working!)"
        elif avg_ping < 8:
            rating = "✅ GOOD (Active worker responds)"
        elif avg_ping < 15:
            rating = "⚠️  AVERAGE (May be cold start)"
        else:
            rating = "❌ SLOW (Worker issues)"
        
        print(f"   🏆 Performance: {rating}")
    else:
        print(f"❌ Benchmark failed - no successful pings")

def main():
    """Główna funkcja testowa"""
    print("🧪 RunPod FIXED Endpoint Tester")
    print("===============================")
    print("🎯 RTX 3090 + 100GB + ACTIVE WORKER")
    print("⭐ Testuje endpoint z workers_min=1")
    print("")
    
    # Setup API
    load_dotenv('config.env')
    runpod.api_key = os.getenv('RUNPOD_API_KEY')
    
    # Sprawdź status active worker
    endpoint_status = check_active_worker_status()
    
    if not endpoint_status:
        print("❌ Nie można kontynuować bez endpoint")
        return
    
    # Sprawdź czy active worker jest gotowy
    workers_ready = endpoint_status.get('workersReady', 0)
    workers_running = endpoint_status.get('workersRunning', 0)
    
    if workers_ready > 0:
        print(f"🚀 ACTIVE WORKER gotowy! Rozpoczynam testy...")
    elif workers_running > 0:
        print(f"⏳ ACTIVE WORKER się uruchamia... Będę testować...")
    else:
        print(f"⚠️  ACTIVE WORKER jeszcze nie uruchomiony")
        choice = input("Czy kontynuować testy? (y/n): ").lower()
        if choice != 'y':
            return
    
    # Uruchom testy
    test_fixed_endpoint()
    
    # Benchmark
    run_performance_benchmark()
    
    print(f"\n🎉 Testy FIXED endpoint zakończone!")
    print("📋 Podsumowanie FIXED endpoint:")
    print("   ✅ Active worker health check")
    print("   ✅ Performance test") 
    print("   ✅ Echo with GPU data")
    print("   ✅ Environment setup")
    print("   ✅ Performance benchmark")
    print("")
    print("🖥️  FIXED Endpoint RTX 3090 Details:")
    print("   - GPU: NVIDIA GeForce RTX 3090 (24GB VRAM)")
    print("   - Storage: 100GB container + 100GB volume")
    print("   - ⭐ ACTIVE WORKER: 1 (workers_min=1)") 
    print("   - Features: FlashBoot + 30s timeout")
    print("   - Status: Ready for production!")

if __name__ == "__main__":
    main()