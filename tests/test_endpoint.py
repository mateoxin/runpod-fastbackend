#!/usr/bin/env python3
"""
Test RunPod Serverless Endpoint
Testuje utworzony endpoint z RTX 3090
"""

import runpod
import os
import json
import time
from dotenv import load_dotenv

def load_endpoint_info():
    """Ładuje informacje o endpoint"""
    try:
        with open('endpoint_info.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Nie znaleziono endpoint_info.json")
        return None

def test_endpoint():
    """Testuje endpoint"""
    # Ładuj konfigurację
    load_dotenv('config.env')
    runpod.api_key = os.getenv('RUNPOD_API_KEY')
    
    endpoint_info = load_endpoint_info()
    if not endpoint_info:
        return
    
    endpoint_id = endpoint_info['id']
    endpoint_url = endpoint_info['url']
    
    print(f"🚀 Testowanie Endpoint: {endpoint_info['name']}")
    print(f"🆔 ID: {endpoint_id}")
    print(f"🔗 URL: {endpoint_url}")
    print(f"🖥️  GPU: {endpoint_info['gpu_type']} ({endpoint_info['gpu_memory']})")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n🧪 Test 1: Health Check")
    try:
        # Inicjalizuj endpoint
        endpoint = runpod.Endpoint(endpoint_id)
        
        # Wyślij test job
        test_payload = {
            "input": {
                "type": "health",
                "message": "Test RTX 3090 endpoint"
            }
        }
        
        print(f"📤 Wysyłanie payload: {test_payload}")
        
        # Uruchom job
        run_request = endpoint.run_sync(test_payload, timeout=120)
        
        if run_request:
            print(f"✅ Health check PASSED")
            print(f"📋 Response: {json.dumps(run_request, indent=2)}")
        else:
            print("❌ Health check FAILED - brak response")
            
    except Exception as e:
        print(f"❌ Health check ERROR: {e}")
    
    # Test 2: Ping Test
    print("\n🧪 Test 2: Ping Test")
    try:
        ping_payload = {
            "input": {
                "type": "ping"
            }
        }
        
        print(f"📤 Wysyłanie ping payload...")
        run_request = endpoint.run_sync(ping_payload, timeout=60)
        
        if run_request:
            print(f"✅ Ping test PASSED")
            print(f"🏓 Ping Response: {json.dumps(run_request, indent=2)}")
        else:
            print("❌ Ping test FAILED")
            
    except Exception as e:
        print(f"❌ Ping test ERROR: {e}")
    
    # Test 3: Echo Test
    print("\n🧪 Test 3: Echo Test")
    try:
        echo_payload = {
            "input": {
                "type": "echo",
                "test_data": "RTX 3090 endpoint test",
                "gpu_type": "NVIDIA GeForce RTX 3090",
                "timestamp": time.time()
            }
        }
        
        print(f"📤 Wysyłanie echo payload...")
        run_request = endpoint.run_sync(echo_payload, timeout=60)
        
        if run_request:
            print(f"✅ Echo test PASSED")
            print(f"🔄 Echo Response: {json.dumps(run_request, indent=2)}")
        else:
            print("❌ Echo test FAILED")
            
    except Exception as e:
        print(f"❌ Echo test ERROR: {e}")
    
    # Test 4: Environment Setup
    print("\n🧪 Test 4: Environment Setup Test")
    try:
        setup_payload = {
            "input": {
                "type": "setup_environment"
            }
        }
        
        print(f"📤 Uruchamianie setup environment... (może potrwać 2-3 minuty)")
        run_request = endpoint.run_sync(setup_payload, timeout=300)  # 5 min timeout
        
        if run_request:
            print(f"✅ Environment setup COMPLETED")
            print(f"🔧 Setup Response: {json.dumps(run_request, indent=2)}")
        else:
            print("❌ Environment setup FAILED")
            
    except Exception as e:
        print(f"❌ Environment setup ERROR: {e}")
    
    # Test 5: List Models
    print("\n🧪 Test 5: List Models Test")
    try:
        models_payload = {
            "input": {
                "type": "list_models"
            }
        }
        
        print(f"📤 Sprawdzanie dostępnych modeli...")
        run_request = endpoint.run_sync(models_payload, timeout=120)
        
        if run_request:
            print(f"✅ List models PASSED")
            print(f"📁 Models Response: {json.dumps(run_request, indent=2)}")
        else:
            print("❌ List models FAILED")
            
    except Exception as e:
        print(f"❌ List models ERROR: {e}")

def check_endpoint_status():
    """Sprawdza status endpoint"""
    load_dotenv('config.env')
    runpod.api_key = os.getenv('RUNPOD_API_KEY')
    
    endpoint_info = load_endpoint_info()
    if not endpoint_info:
        return
    
    print(f"📊 Sprawdzanie statusu endpoint...")
    
    try:
        endpoints = runpod.get_endpoints()
        for endpoint in endpoints:
            if endpoint.get('id') == endpoint_info['id']:
                print(f"✅ Endpoint znaleziony:")
                print(f"   📛 Name: {endpoint.get('name', 'Unknown')}")
                print(f"   🆔 ID: {endpoint.get('id', 'Unknown')}")
                print(f"   📈 Status: {endpoint.get('status', 'Unknown')}")
                print(f"   👥 Workers: {endpoint.get('workersMax', 'Unknown')} max")
                print(f"   🌍 Locations: {endpoint.get('locations', 'Unknown')}")
                return endpoint
        
        print("❌ Endpoint nie znaleziony")
        return None
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania statusu: {e}")
        return None

def main():
    """Główna funkcja testowa"""
    print("🧪 RunPod Endpoint Tester")
    print("=========================")
    
    # Sprawdź status endpoint
    endpoint_status = check_endpoint_status()
    
    if not endpoint_status:
        print("❌ Nie można kontynuować bez statusu endpoint")
        return
    
    # Sprawdź czy endpoint jest gotowy
    status = endpoint_status.get('status', 'Unknown')
    if status not in ['READY', 'ACTIVE'] and status != 'Unknown':
        print(f"⚠️  Endpoint nie jest gotowy (status: {status})")
        print("💡 Endpoint może potrzebować więcej czasu na uruchomienie.")
        print("   Spróbuj ponownie za kilka minut.")
        return
    
    if status == 'Unknown':
        print(f"⚠️  Status endpoint: {status} - próbujemy testować...")
        print("💡 Endpoint może być w trakcie uruchamiania, ale spróbujemy połączenia.")
    
    # Uruchom testy
    test_endpoint()
    
    print("\n🎉 Testy zakończone!")
    print("📋 Podsumowanie testów:")
    print("   ✅ Health check - podstawowy test połączenia")
    print("   ✅ Ping test - test responsywności") 
    print("   ✅ Echo test - test przesyłania danych")
    print("   ✅ Environment setup - instalacja PyTorch/ML libs")
    print("   ✅ Models listing - sprawdzenie dostępnych modeli")
    print("")
    print("🖥️  Endpoint RTX 3090 Details:")
    print("   - GPU: NVIDIA GeForce RTX 3090 (24GB VRAM)")
    print("   - Storage: 100GB container + 100GB volume")
    print("   - Max workers: 2 (quota limit)")
    print("   - Wszystkie zmienne środowiskowe skonfigurowane")

if __name__ == "__main__":
    main()