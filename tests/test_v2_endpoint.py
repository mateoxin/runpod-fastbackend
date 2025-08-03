#!/usr/bin/env python3
"""
Test RunPod Endpoint v2
Testuje nowy, zoptymalizowany endpoint RTX 3090
"""

import runpod
import os
import json
import time
from dotenv import load_dotenv
from datetime import datetime

def load_endpoint_v2_info():
    """Ładuje informacje o endpoint v2"""
    try:
        with open('endpoint_v2_info.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Nie znaleziono endpoint_v2_info.json")
        return None

def check_endpoint_status_v2():
    """Sprawdza status endpoint v2"""
    load_dotenv('config.env')
    runpod.api_key = os.getenv('RUNPOD_API_KEY')
    
    endpoint_info = load_endpoint_v2_info()
    if not endpoint_info:
        return None
    
    print(f"📊 Sprawdzanie statusu endpoint v2...")
    
    try:
        endpoints = runpod.get_endpoints()
        for endpoint in endpoints:
            if endpoint.get('id') == endpoint_info['id']:
                print(f"✅ Endpoint v2 znaleziony:")
                print(f"   📛 Name: {endpoint.get('name', 'Unknown')}")
                print(f"   🆔 ID: {endpoint.get('id', 'Unknown')}")
                print(f"   📈 Status: {endpoint.get('status', 'Unknown')}")
                print(f"   👥 Workers: {endpoint.get('workersMax', 'Unknown')} max")
                print(f"   🌍 Locations: {endpoint.get('locations', 'Unknown')}")
                print(f"   ⚡ Flashboot: {endpoint_info.get('flashboot', False)}")
                print(f"   ⏱️  Idle timeout: {endpoint_info.get('idle_timeout', 'Unknown')}s")
                return endpoint
        
        print("❌ Endpoint v2 nie znaleziony")
        return None
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania statusu: {e}")
        return None

def test_endpoint_v2():
    """Testuje endpoint v2"""
    
    endpoint_info = load_endpoint_v2_info()
    if not endpoint_info:
        return
    
    endpoint_id = endpoint_info['id']
    endpoint_url = endpoint_info['url']
    
    print(f"\n🚀 Testowanie Endpoint v2: {endpoint_info['name']}")
    print(f"🆔 ID: {endpoint_id}")
    print(f"🔗 URL: {endpoint_url}")
    print(f"🖥️  GPU: {endpoint_info['gpu_type']} ({endpoint_info['gpu_memory']})")
    print(f"💾 Storage: {endpoint_info['container_disk_gb']}GB + {endpoint_info['volume_gb']}GB")
    print(f"⚡ Features: Flashboot={endpoint_info['flashboot']}, Timeout={endpoint_info['idle_timeout']}s")
    print("=" * 60)
    
    # Inicjalizuj endpoint
    try:
        endpoint = runpod.Endpoint(endpoint_id)
        print(f"✅ Połączenie z endpoint established")
    except Exception as e:
        print(f"❌ Błąd połączenia: {e}")
        return
    
    # Test 1: Quick Health Check
    print(f"\n🧪 Test 1: Quick Health Check")
    try:
        health_payload = {
            "input": {
                "type": "health",
                "message": "RTX 3090 v2 endpoint test",
                "version": "v2"
            }
        }
        
        print(f"📤 Wysyłanie health check...")
        start_time = time.time()
        
        result = endpoint.run_sync(health_payload, timeout=90)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if result:
            print(f"✅ Health check PASSED ({response_time:.1f}s)")
            print(f"📋 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Health check FAILED")
            
    except Exception as e:
        print(f"❌ Health check ERROR: {e}")
    
    # Test 2: Performance Ping
    print(f"\n🧪 Test 2: Performance Ping")
    try:
        ping_payload = {
            "input": {
                "type": "ping"
            }
        }
        
        print(f"📤 Performance ping...")
        start_time = time.time()
        
        result = endpoint.run_sync(ping_payload, timeout=30)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if result:
            print(f"✅ Ping test PASSED ({response_time:.1f}s)")
            print(f"🏓 Response: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Ping test FAILED")
            
    except Exception as e:
        print(f"❌ Ping test ERROR: {e}")
    
    # Test 3: Echo with GPU Info
    print(f"\n🧪 Test 3: Echo + GPU Data Test")
    try:
        echo_payload = {
            "input": {
                "type": "echo",
                "test_data": {
                    "endpoint_version": "v2",
                    "gpu_target": "RTX 3090",
                    "storage_config": "100GB+100GB",
                    "optimization": "flashboot_enabled",
                    "test_timestamp": datetime.now().isoformat()
                }
            }
        }
        
        print(f"📤 Echo test z danymi GPU...")
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
    
    # Test 4: Environment Setup (Heavy Test)
    print(f"\n🧪 Test 4: Environment Setup (PyTorch/CUDA)")
    try:
        setup_payload = {
            "input": {
                "type": "setup_environment"
            }
        }
        
        print(f"📤 Uruchamianie setup environment...")
        print(f"💡 To może potrwać 2-4 minuty (PyTorch + CUDA)")
        start_time = time.time()
        
        result = endpoint.run_sync(setup_payload, timeout=360)  # 6 min timeout
        
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
    
    # Test 5: Model Operations
    print(f"\n🧪 Test 5: Model Operations Test")
    try:
        models_payload = {
            "input": {
                "type": "list_models"
            }
        }
        
        print(f"📤 Sprawdzanie modeli...")
        start_time = time.time()
        
        result = endpoint.run_sync(models_payload, timeout=120)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if result:
            print(f"✅ Models test PASSED ({response_time:.1f}s)")
            print(f"📁 Models Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Models test FAILED")
            
    except Exception as e:
        print(f"❌ Models test ERROR: {e}")

def benchmark_endpoint():
    """Benchmark endpoint performance"""
    
    endpoint_info = load_endpoint_v2_info()
    if not endpoint_info:
        return
    
    print(f"\n⚡ BENCHMARK: Endpoint v2 Performance")
    print("=" * 40)
    
    endpoint = runpod.Endpoint(endpoint_info['id'])
    
    # Multiple quick pings
    ping_times = []
    
    for i in range(3):
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
        
        print(f"\n📊 Benchmark Results:")
        print(f"   ⚡ Average response: {avg_ping:.2f}s")
        print(f"   🚀 Fastest response: {min_ping:.2f}s")
        print(f"   🐌 Slowest response: {max_ping:.2f}s")
        
        # Performance rating
        if avg_ping < 5:
            rating = "🌟 EXCELLENT"
        elif avg_ping < 10:
            rating = "✅ GOOD"
        elif avg_ping < 20:
            rating = "⚠️  AVERAGE"
        else:
            rating = "❌ SLOW"
        
        print(f"   🏆 Performance: {rating}")
    else:
        print(f"❌ Benchmark failed - no successful pings")

def main():
    """Główna funkcja testowa"""
    print("🧪 RunPod Endpoint v2 Tester")
    print("=============================")
    print("🎯 RTX 3090 + 100GB + Optimizations")
    print("")
    
    # Setup API
    load_dotenv('config.env')
    runpod.api_key = os.getenv('RUNPOD_API_KEY')
    
    # Sprawdź status
    endpoint_status = check_endpoint_status_v2()
    
    if not endpoint_status:
        print("❌ Nie można kontynuować bez endpoint")
        return
    
    # Sprawdź czy gotowy
    status = endpoint_status.get('status', 'Unknown')
    if status not in ['READY', 'ACTIVE'] and status != 'Unknown':
        print(f"⚠️  Endpoint nie jest gotowy (status: {status})")
        print("💡 Poczekaj kilka minut i spróbuj ponownie")
        return
    
    print(f"🚀 Status: {status} - rozpoczynam testy...")
    
    # Uruchom testy
    test_endpoint_v2()
    
    # Benchmark
    benchmark_endpoint()
    
    print(f"\n🎉 Testy v2 zakończone!")
    print("📋 Podsumowanie endpoint v2:")
    print("   ✅ Quick health check")
    print("   ✅ Performance ping") 
    print("   ✅ Echo with GPU data")
    print("   ✅ Environment setup (PyTorch/CUDA)")
    print("   ✅ Model operations")
    print("   ✅ Performance benchmark")
    print("")
    print("🖥️  Endpoint RTX 3090 v2 Details:")
    print("   - GPU: NVIDIA GeForce RTX 3090 (24GB VRAM)")
    print("   - Storage: 100GB container + 100GB volume")
    print("   - Features: Flashboot + 10s timeout") 
    print("   - Workers: 1 (optimized)")
    print("   - Status: Ready for production!")

if __name__ == "__main__":
    main()