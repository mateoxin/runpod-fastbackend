#!/usr/bin/env python3
"""
Tworzenie DZIAŁAJĄCEGO RunPod Endpoint
Z najlepszym dostępnym GPU i gwarantowanym active worker
"""

import runpod
import os
import json
import time
from dotenv import load_dotenv
from datetime import datetime

def setup_runpod():
    """Konfiguracja RunPod"""
    load_dotenv('config.env')
    runpod.api_key = os.getenv('RUNPOD_API_KEY')
    
    if not runpod.api_key:
        raise ValueError("RUNPOD_API_KEY nie jest ustawiony!")
    
    print(f"✅ RunPod API skonfigurowany: {runpod.api_key[:10]}...")
    return True

def find_best_available_gpu():
    """Znajduje najlepszą dostępną kartę GPU"""
    
    print("\n🔍 Szukanie najlepszej dostępnej karty GPU...")
    
    # Lista preferencji GPU (od najlepszych)
    gpu_preferences = [
        'NVIDIA GeForce RTX 5090',  # 32GB VRAM - najnowsza
        'NVIDIA GeForce RTX 4090',  # 24GB VRAM - sprawdzona
        'NVIDIA GeForce RTX 3090',  # 24GB VRAM - nasza pierwotna opcja
        'NVIDIA GeForce RTX 4080 SUPER',  # 16GB VRAM
        'NVIDIA GeForce RTX 4080',  # 16GB VRAM  
        'NVIDIA RTX A5000',        # 24GB VRAM - workstation
        'NVIDIA RTX A4500'         # 20GB VRAM - backup
    ]
    
    try:
        gpus = runpod.get_gpus()
        available_gpus = {gpu['id']: gpu for gpu in gpus}
        
        print("📊 Sprawdzanie preferencji GPU:")
        for gpu_id in gpu_preferences:
            if gpu_id in available_gpus:
                gpu_info = available_gpus[gpu_id]
                print(f"  ✅ {gpu_info['displayName']} ({gpu_info['memoryInGb']}GB) - DOSTĘPNE")
                return gpu_id, gpu_info
            else:
                print(f"  ❌ {gpu_id} - niedostępne")
        
        print("⚠️  Żadne preferowane GPU nie jest dostępne, używam pierwszego dostępnego...")
        if gpus:
            gpu_info = gpus[0]
            return gpu_info['id'], gpu_info
        else:
            print("❌ Brak dostępnych GPU!")
            return None, None
            
    except Exception as e:
        print(f"❌ Błąd sprawdzania GPU: {e}")
        return None, None

def create_working_template(gpu_info):
    """Tworzy template z optymalizacjami dla wybranego GPU"""
    
    gpu_name = gpu_info['displayName'] if gpu_info else 'Unknown'
    gpu_memory = gpu_info['memoryInGb'] if gpu_info else 'Unknown'
    
    # Zmienne środowiskowe
    env_vars = {
        'RUNPOD_API_KEY': os.getenv('RUNPOD_API_KEY'),
        'HF_TOKEN': os.getenv('HF_TOKEN'), 
        'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN'),
        'PYTHONUNBUFFERED': '1',
        'HANDLER_FILE': 'handler_fast.py',
        'CUDA_VISIBLE_DEVICES': '0',
        'NVIDIA_VISIBLE_DEVICES': 'all',
        'NVIDIA_DRIVER_CAPABILITIES': 'compute,utility',
        'RUNPOD_INIT_TIMEOUT': '900',   # 15 min timeout
        'MAX_WORKERS': '1',
        'TIMEOUT': '1200',  # 20 min timeout
        'MEMORY_LIMIT': '100G'
    }
    
    print(f"\n📋 Tworzenie template dla {gpu_name}...")
    print("🔧 Konfiguracja:")
    print("   - Image: PyTorch 2.1.0 + CUDA 11.8")
    print("   - Container Disk: 100GB")
    print("   - Volume: 100GB") 
    print(f"   - Target GPU: {gpu_name} ({gpu_memory}GB)")
    print("   - Init timeout: 15 min")
    print(f"   - Env vars: {len(env_vars)}")
    
    try:
        template_response = runpod.create_template(
            name=f'fastbackend-{gpu_name.lower().replace(" ", "-")}-template',
            image_name='runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04',
            docker_start_cmd='python3 handler_fast.py',
            container_disk_in_gb=100,
            volume_in_gb=100,
            volume_mount_path='/workspace',
            ports='8000/http,22/tcp',
            env=env_vars,
            is_serverless=True
        )
        
        if template_response:
            template_id = template_response.get('id')
            print(f"✅ Template utworzony: {template_id}")
            return template_id
        else:
            print("❌ Błąd tworzenia template")
            return None
            
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return None

def create_guaranteed_endpoint(template_id, gpu_id, gpu_info):
    """Tworzy endpoint z gwarancją działania"""
    
    gpu_name = gpu_info['displayName']
    gpu_memory = gpu_info['memoryInGb']
    
    print(f"\n🚀 Tworzenie GWARANTOWANEGO endpoint...")
    print("📊 Optymalne parametry:")
    print(f"   - GPU: {gpu_name} ({gpu_memory}GB VRAM)")
    print("   - Template: Zoptymalizowany")
    print("   - ⭐ WORKERS_MIN: 1 (ACTIVE WORKER)")
    print("   - Workers max: 1")
    print("   - Storage: 100GB")
    print("   - Idle timeout: 60s (dłuższy)")
    print("   - FlashBoot: enabled")
    print("   - Locations: US,EU (multi-region)")
    
    try:
        response = runpod.create_endpoint(
            name=f'fastbackend-{gpu_name.lower().replace(" ", "-")}-working',
            template_id=template_id,
            gpu_ids=gpu_id,
            locations='US,EU',        # Multi-region dla dostępności
            idle_timeout=60,          # Dłuższy timeout
            scaler_type='QUEUE_DELAY',
            scaler_value=3,           # Szybka reakcja
            workers_min=1,            # 🎯 ACTIVE WORKER!
            workers_max=1,            # Pojedynczy worker
            gpu_count=1,              # 1 GPU per worker
            flashboot=True            # FlashBoot enabled
        )
        
        if response:
            endpoint_id = response.get('id') if isinstance(response, dict) else response
            
            print(f"\n✅ WORKING endpoint utworzony!")
            print(f"🆔 ID: {endpoint_id}")
            print(f"📛 Name: fastbackend-{gpu_name.lower().replace(' ', '-')}-working")
            print(f"🔗 URL: https://api.runpod.ai/v2/{endpoint_id}")
            print(f"⭐ ACTIVE WORKER z {gpu_name}!")
            
            # Zapisz informacje
            endpoint_info = {
                'id': endpoint_id,
                'name': f'fastbackend-{gpu_name.lower().replace(" ", "-")}-working',
                'url': f'https://api.runpod.ai/v2/{endpoint_id}',
                'template_id': template_id,
                'gpu_type': gpu_id,
                'gpu_name': gpu_name,
                'gpu_memory': f'{gpu_memory}GB',
                'container_disk_gb': 100,
                'volume_gb': 100,
                'workers_min': 1,
                'workers_max': 1,
                'idle_timeout': 60,
                'flashboot': True,
                'version': 'working',
                'has_active_worker': True,
                'created_at': datetime.now().isoformat(),
                'status': 'creating'
            }
            
            # Zapisz do pliku
            with open('endpoint_working_info.json', 'w') as f:
                json.dump(endpoint_info, f, indent=2)
            
            print(f"💾 Informacje zapisane w endpoint_working_info.json")
            return endpoint_id
            
        else:
            print("❌ Błąd tworzenia endpoint")
            return None
            
    except Exception as e:
        print(f"❌ Błąd endpoint: {e}")
        return None

def wait_and_verify_worker(endpoint_id, timeout=900):
    """Czeka i weryfikuje uruchomienie active worker"""
    
    print(f"\n⏳ Monitorowanie active worker w endpoint {endpoint_id}...")
    print("💡 Maksymalny czas oczekiwania: 15 minut")
    
    start_time = time.time()
    last_status = None
    
    while time.time() - start_time < timeout:
        try:
            endpoints = runpod.get_endpoints()
            for endpoint in endpoints:
                if endpoint.get('id') == endpoint_id:
                    status = endpoint.get('status', 'Unknown')
                    workers_ready = endpoint.get('workersReady', 0)
                    workers_running = endpoint.get('workersRunning', 0)
                    workers_init = endpoint.get('workersInitializing', 0)
                    
                    # Pokazuj zmiany statusu
                    if status != last_status:
                        print(f"📊 Status change: {last_status} → {status}")
                        last_status = status
                    
                    print(f"👥 Workers - Ready: {workers_ready}, Running: {workers_running}, Init: {workers_init}")
                    
                    if status in ['READY', 'ACTIVE'] and workers_ready > 0:
                        print(f"🎉 ACTIVE WORKER gotowy! Status: {status}")
                        return True
                    elif status in ['FAILED', 'ERROR']:
                        print(f"❌ Endpoint failed! Status: {status}")
                        return False
                    elif workers_running > 0 or workers_init > 0:
                        print(f"⏳ Worker się uruchamia...")
                    
                    break
            
            print("⏳ Sprawdzanie za 45s...")
            time.sleep(45)
            
        except Exception as e:
            print(f"⚠️  Błąd monitorowania: {e}")
            time.sleep(45)
    
    print(f"⚠️  Timeout po {timeout//60} minutach")
    return False

def main():
    """Główna funkcja"""
    print("🚀 RunPod WORKING Endpoint Creator")
    print("===================================")
    print("🎯 Cel: Najlepsze GPU + 100GB + GWARANTOWANY ACTIVE WORKER")
    print("💡 Strategia: Znajdź najlepszą dostępną kartę i utwórz stabilny endpoint")
    print("")
    
    # Setup RunPod
    if not setup_runpod():
        return
    
    # Znajdź najlepsze dostępne GPU
    gpu_id, gpu_info = find_best_available_gpu()
    if not gpu_id:
        print("❌ Nie można znaleźć dostępnego GPU")
        return
    
    print(f"\n🎯 Wybrane GPU: {gpu_info['displayName']} ({gpu_info['memoryInGb']}GB)")
    
    # Utwórz template
    template_id = create_working_template(gpu_info)
    if not template_id:
        print("❌ Nie udało się utworzyć template")
        return
    
    # Utwórz working endpoint
    endpoint_id = create_guaranteed_endpoint(template_id, gpu_id, gpu_info)
    if not endpoint_id:
        print("❌ Nie udało się utworzyć endpoint")
        return
    
    print(f"\n🎯 WORKING endpoint utworzony!")
    print(f"🆔 ID: {endpoint_id}")
    print(f"🖥️  GPU: {gpu_info['displayName']} ({gpu_info['memoryInGb']}GB)")
    print(f"📁 Szczegóły w: endpoint_working_info.json")
    print("")
    print("📋 Następne kroki:")
    print("1. Active worker uruchomi się automatycznie")
    print("2. Poczekaj na gotowość (maks 15 min)")
    print("3. Uruchom: python test_working_endpoint.py")
    
    # Opcjonalnie czekaj na uruchomienie
    choice = input("\nCzy czekać na uruchomienie active worker? (y/n): ").lower()
    if choice == 'y':
        if wait_and_verify_worker(endpoint_id):
            print("\n🎉 ENDPOINT GOTOWY DO TESTOWANIA!")
        else:
            print("\n⚠️  Endpoint może potrzebować więcej czasu")

if __name__ == "__main__":
    main()