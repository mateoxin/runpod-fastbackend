#!/usr/bin/env python3
"""
RunPod Serverless Endpoint Creator
Tworzy endpoint z RTX 3090, 100GB RAM i wszystkimi zmiennymi środowiskowymi
"""

import runpod
import os
from dotenv import load_dotenv
import json

# Ładowanie zmiennych środowiskowych
load_dotenv('config.env')

def setup_runpod_client():
    """Konfiguracja klienta RunPod"""
    api_key = os.getenv('RUNPOD_API_KEY')
    if not api_key:
        raise ValueError("RUNPOD_API_KEY nie został ustawiony!")
    
    runpod.api_key = api_key
    print(f"✅ RunPod API Key skonfigurowany: {api_key[:10]}...")
    return True

def get_gpu_types():
    """Pobiera dostępne typy GPU"""
    try:
        gpu_types = runpod.get_gpu_types()
        print("\n🖥️  Dostępne typy GPU:")
        for gpu in gpu_types:
            if 'RTX 3090' in gpu.get('displayName', '') or '3090' in gpu.get('id', ''):
                print(f"  ✅ {gpu.get('displayName', 'Unknown')}: {gpu.get('id', 'Unknown ID')}")
                print(f"     Memory: {gpu.get('memoryInGb', 'Unknown')} GB")
                print(f"     Max pods: {gpu.get('maxQuantity', 'Unknown')}")
        return gpu_types
    except Exception as e:
        print(f"❌ Błąd pobierania typów GPU: {e}")
        return []

def create_template():
    """Tworzy template dla endpoint"""
    
    # Zmienne środowiskowe dla template
    environment_variables = {
        'RUNPOD_API_KEY': os.getenv('RUNPOD_API_KEY'),
        'HF_TOKEN': os.getenv('HF_TOKEN'),
        'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN'),
        'PYTHONUNBUFFERED': '1',
        'HANDLER_FILE': 'handler_fast.py',
        'MAX_WORKERS': '1',
        'TIMEOUT': '300',
        'MEMORY_LIMIT': '100G'
    }
    
    # Konfiguracja template
    template_config = {
        'name': 'fastbackend-rtx3090-template',
        'image_name': 'runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04',
        'docker_start_cmd': 'python3 handler_fast.py',
        'container_disk_in_gb': 100,  # 100GB storage
        'volume_in_gb': 100,  # 100GB volume
        'volume_mount_path': '/workspace',
        'ports': '8000/http,22/tcp',
        'env': environment_variables,
        'is_serverless': True
    }
    
    try:
        print("\n📋 Tworzenie Template...")
        print(f"📊 Konfiguracja template:")
        print(f"   - Image: PyTorch 2.1.0")
        print(f"   - Storage: 100GB")
        print(f"   - Volume: 100GB")
        print(f"   - Zmienne środowiskowe: {len(environment_variables)}")
        
        # Tworzenie template
        template_response = runpod.create_template(**template_config)
        
        if template_response:
            template_id = template_response.get('id')
            print(f"✅ Template utworzony: {template_id}")
            return template_id
        else:
            print("❌ Nie udało się utworzyć template")
            return None
            
    except Exception as e:
        print(f"❌ Błąd tworzenia template: {e}")
        return None

def create_serverless_endpoint(template_id):
    """Tworzy serverless endpoint z RTX 3090"""
    
    try:
        print("\n🚀 Tworzenie Serverless Endpoint...")
        print(f"📊 Konfiguracja:")
        print(f"   - GPU: RTX 3090 (24GB VRAM)")
        print(f"   - Template ID: {template_id}")
        print(f"   - Max Workers: 2 (quota limit)")
        print(f"   - Locations: US, EU")
        
        # Tworzenie endpoint z poprawnymi parametrami
        response = runpod.create_endpoint(
            name='fastbackend-rtx3090-endpoint',
            template_id=template_id,
            gpu_ids='NVIDIA GeForce RTX 3090',  # Użyj pełnej nazwy GPU
            locations='US,EU',  # Preferowane lokalizacje
            idle_timeout=5,  # 5 sekund timeout
            scaler_type='QUEUE_DELAY',
            scaler_value=10,
            workers_min=0,   # Min 0 (auto-scale)
            workers_max=2,   # Max 2 workers (quota limit)
            gpu_count=1      # 1 GPU per worker
        )
        
        if response:
            endpoint_id = response.get('id') if isinstance(response, dict) else response
            print(f"\n✅ Endpoint utworzony pomyślnie!")
            print(f"🆔 ID: {endpoint_id}")
            print(f"📛 Name: fastbackend-rtx3090-endpoint")
            print(f"🔗 URL: https://api.runpod.ai/v2/{endpoint_id}")
            
            # Zapisz informacje o endpoint
            endpoint_info = {
                'id': endpoint_id,
                'name': 'fastbackend-rtx3090-endpoint',
                'url': f"https://api.runpod.ai/v2/{endpoint_id}",
                'template_id': template_id,
                'gpu_type': 'NVIDIA GeForce RTX 3090',
                'gpu_memory': '24GB',
                'storage_gb': 100,
                'workers_max': 3,
                'created_at': 'now'
            }
            
            with open('endpoint_info.json', 'w') as f:
                json.dump(endpoint_info, f, indent=2)
            
            print(f"💾 Informacje zapisane w endpoint_info.json")
            return response
        else:
            print("❌ Nie udało się utworzyć endpoint")
            return None
            
    except Exception as e:
        print(f"❌ Błąd tworzenia endpoint: {e}")
        return None

def list_existing_endpoints():
    """Lista istniejących endpoints"""
    try:
        endpoints = runpod.get_endpoints()
        print(f"\n📋 Istniejące endpoints ({len(endpoints)}):")
        for endpoint in endpoints:
            print(f"  🔸 {endpoint.get('name', 'Unknown')} ({endpoint.get('id', 'Unknown')})")
            print(f"     Status: {endpoint.get('status', 'Unknown')}")
            print(f"     GPU: {endpoint.get('template', {}).get('gpuIds', 'Unknown')}")
        return endpoints
    except Exception as e:
        print(f"❌ Błąd pobierania endpoints: {e}")
        return []

def main():
    """Główna funkcja"""
    print("🚀 RunPod Serverless Endpoint Creator")
    print("=====================================")
    
    # Setup klienta RunPod
    if not setup_runpod_client():
        return
    
    # Pobierz dostępne GPU
    gpu_types = get_gpu_types()
    
    # Lista istniejących endpoints
    existing_endpoints = list_existing_endpoints()
    
    # Sprawdź czy endpoint już istnieje
    existing_names = [ep.get('name', '') for ep in existing_endpoints]
    if 'fastbackend-rtx3090-endpoint' in existing_names:
        print("\n⚠️  Endpoint 'fastbackend-rtx3090-endpoint' już istnieje!")
        print("Czy chcesz kontynuować i utworzyć nowy? (Ctrl+C aby anulować)")
        input("Naciśnij Enter aby kontynuować...")
    
    # Utwórz template
    template_id = create_template()
    if not template_id:
        print("\n❌ Nie udało się utworzyć template - przerywam")
        return
    
    # Utwórz endpoint używając template
    endpoint = create_serverless_endpoint(template_id)
    
    if endpoint:
        print("\n🎉 Endpoint gotowy do użycia!")
        print("📋 Następne kroki:")
        print("   1. Zaczekaj aż endpoint się uruchomi (~2-5 min)")
        print("   2. Przetestuj endpoint używając ID z endpoint_info.json")
        print("   3. Użyj w swoich aplikacjach")
        print("   4. Pamiętaj o kosztach - endpoint będzie naliczał opłaty!")
    else:
        print("\n❌ Nie udało się utworzyć endpoint")

if __name__ == "__main__":
    main()