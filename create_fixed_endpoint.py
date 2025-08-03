#!/usr/bin/env python3
"""
Tworzenie POPRAWNEGO RunPod Endpoint
Z RTX 3090, 100GB dysku i ACTIVE WORKERS (workers_min=1)
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

def create_fixed_template():
    """Tworzy template z optymalizacjami dla active workers"""
    
    # Zmienne środowiskowe dla endpoint
    env_vars = {
        'RUNPOD_API_KEY': os.getenv('RUNPOD_API_KEY'),
        'HF_TOKEN': os.getenv('HF_TOKEN'), 
        'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN'),
        'PYTHONUNBUFFERED': '1',
        'HANDLER_FILE': 'handler_fast.py',
        'CUDA_VISIBLE_DEVICES': '0',
        'NVIDIA_VISIBLE_DEVICES': 'all',
        'NVIDIA_DRIVER_CAPABILITIES': 'compute,utility',
        'TORCH_CUDA_ARCH_LIST': '8.6',  # RTX 3090 architecture
        'RUNPOD_INIT_TIMEOUT': '600',   # 10 min timeout dla cold start
        'MAX_WORKERS': '1',
        'TIMEOUT': '900',  # 15 min timeout
        'MEMORY_LIMIT': '100G'
    }
    
    print("\n📋 Tworzenie FIXED template...")
    print("🔧 Konfiguracja:")
    print("   - Image: PyTorch 2.1.0 + CUDA 11.8")
    print("   - Container Disk: 100GB")
    print("   - Volume: 100GB") 
    print("   - GPU: RTX 3090 optimized")
    print("   - Init timeout: 10 min")
    print(f"   - Env vars: {len(env_vars)}")
    
    try:
        template_response = runpod.create_template(
            name='fastbackend-rtx3090-fixed-template',
            image_name='runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04',
            docker_start_cmd='python3 handler_fast.py',
            container_disk_in_gb=100,  # 100GB container disk
            volume_in_gb=100,          # 100GB volume
            volume_mount_path='/workspace',
            ports='8000/http,22/tcp',
            env=env_vars,
            is_serverless=True
        )
        
        if template_response:
            template_id = template_response.get('id')
            print(f"✅ FIXED Template utworzony: {template_id}")
            return template_id
        else:
            print("❌ Błąd tworzenia template")
            return None
            
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return None

def create_working_endpoint(template_id):
    """Tworzy endpoint z ACTIVE WORKERS (workers_min=1)"""
    
    print(f"\n🚀 Tworzenie endpoint z ACTIVE WORKERS...")
    print("📊 KLUCZOWE Parametry:")
    print("   - GPU: RTX 3090 (24GB VRAM)")
    print("   - Template: FIXED")
    print("   - ⭐ WORKERS_MIN: 1 (ACTIVE WORKER!)")
    print("   - Workers max: 1")
    print("   - Storage: 100GB")
    print("   - Idle timeout: 30s")
    print("   - FlashBoot: enabled")
    
    try:
        # KLUCZOWE: workers_min=1 tworzy active worker!
        response = runpod.create_endpoint(
            name='fastbackend-rtx3090-fixed',
            template_id=template_id,
            gpu_ids='NVIDIA GeForce RTX 3090',
            locations='US,EU',
            idle_timeout=30,          # 30s timeout
            scaler_type='QUEUE_DELAY',
            scaler_value=4,           # Default value
            workers_min=1,            # 🎯 ACTIVE WORKER!
            workers_max=1,            # Max 1 worker
            gpu_count=1,              # 1 GPU per worker
            flashboot=True            # FlashBoot enabled
        )
        
        if response:
            endpoint_id = response.get('id') if isinstance(response, dict) else response
            
            print(f"\n✅ FIXED endpoint utworzony!")
            print(f"🆔 ID: {endpoint_id}")
            print(f"📛 Name: fastbackend-rtx3090-fixed")
            print(f"🔗 URL: https://api.runpod.ai/v2/{endpoint_id}")
            print(f"⭐ ACTIVE WORKER: 1 (powinien się uruchomić!)")
            
            # Zapisz informacje
            endpoint_info = {
                'id': endpoint_id,
                'name': 'fastbackend-rtx3090-fixed',
                'url': f'https://api.runpod.ai/v2/{endpoint_id}',
                'template_id': template_id,
                'gpu_type': 'NVIDIA GeForce RTX 3090',
                'gpu_memory': '24GB',
                'container_disk_gb': 100,
                'volume_gb': 100,
                'workers_min': 1,  # ACTIVE WORKER
                'workers_max': 1,
                'idle_timeout': 30,
                'flashboot': True,
                'version': 'fixed',
                'has_active_worker': True,
                'created_at': datetime.now().isoformat(),
                'status': 'creating'
            }
            
            # Zapisz do pliku
            with open('endpoint_fixed_info.json', 'w') as f:
                json.dump(endpoint_info, f, indent=2)
            
            print(f"💾 Informacje zapisane w endpoint_fixed_info.json")
            return endpoint_id
            
        else:
            print("❌ Błąd tworzenia endpoint")
            return None
            
    except Exception as e:
        print(f"❌ Błąd endpoint: {e}")
        return None

def wait_for_active_worker(endpoint_id, timeout=600):
    """Czeka na uruchomienie active worker"""
    
    print(f"\n⏳ Czekanie na ACTIVE WORKER w endpoint {endpoint_id}...")
    print("💡 Active worker powinien uruchomić się w 2-5 minut")
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            endpoints = runpod.get_endpoints()
            for endpoint in endpoints:
                if endpoint.get('id') == endpoint_id:
                    status = endpoint.get('status', 'Unknown')
                    workers_ready = endpoint.get('workersReady', 0)
                    workers_running = endpoint.get('workersRunning', 0)
                    
                    print(f"📊 Status: {status}")
                    print(f"👥 Workers ready: {workers_ready}")
                    print(f"🏃 Workers running: {workers_running}")
                    
                    if status in ['READY', 'ACTIVE'] and workers_ready > 0:
                        print(f"🎉 ACTIVE WORKER gotowy! Status: {status}, Workers: {workers_ready}")
                        return True
                    elif status in ['FAILED', 'ERROR']:
                        print(f"❌ Endpoint ma błąd! Status: {status}")
                        return False
                    
                    break
            
            print("⏳ Sprawdzanie ponownie za 30s...")
            time.sleep(30)
            
        except Exception as e:
            print(f"⚠️  Błąd sprawdzania statusu: {e}")
            time.sleep(30)
    
    print(f"⚠️  Timeout - active worker może nadal się uruchamiać")
    return False

def cleanup_previous_endpoints():
    """Opcjonalnie usuwa poprzednie problematyczne endpoints"""
    
    print(f"\n🧹 Sprawdzanie poprzednich endpoints...")
    
    try:
        endpoints = runpod.get_endpoints()
        problematic_endpoints = [
            '6vi641zor1txhn',  # Pierwszy endpoint
            'n3afussj11mt37'   # Drugi endpoint v2
        ]
        
        for endpoint in endpoints:
            endpoint_id = endpoint.get('id')
            endpoint_name = endpoint.get('name', 'Unknown')
            
            if endpoint_id in problematic_endpoints:
                print(f"🗑️  Znaleziono problematyczny endpoint:")
                print(f"   ID: {endpoint_id}")
                print(f"   Name: {endpoint_name}")
                print(f"   Status: {endpoint.get('status', 'Unknown')}")
                
                choice = input(f"Czy zatrzymać endpoint {endpoint_id}? (y/n): ").lower()
                if choice == 'y':
                    try:
                        print(f"⏹️  Zatrzymywanie endpoint {endpoint_id}...")
                        # runpod.delete_endpoint(endpoint_id)  # Uncomment to delete
                        print(f"✅ Endpoint {endpoint_id} oznaczony do zatrzymania")
                    except Exception as e:
                        print(f"❌ Błąd zatrzymywania: {e}")
        
    except Exception as e:
        print(f"❌ Błąd sprawdzania endpoints: {e}")

def main():
    """Główna funkcja"""
    print("🚀 RunPod FIXED Endpoint Creator")
    print("==================================")
    print("🎯 Cel: RTX 3090 + 100GB + ACTIVE WORKER")
    print("⭐ KLUCZOWE: workers_min=1 dla natychmiastowego uruchomienia")
    print("")
    
    # Setup RunPod
    if not setup_runpod():
        return
    
    # Opcjonalnie posprzątaj stare endpoints
    cleanup_previous_endpoints()
    
    # Utwórz fixed template
    template_id = create_fixed_template()
    if not template_id:
        print("❌ Nie udało się utworzyć template")
        return
    
    # Utwórz working endpoint z active worker
    endpoint_id = create_working_endpoint(template_id)
    if not endpoint_id:
        print("❌ Nie udało się utworzyć endpoint")
        return
    
    # Czekaj na active worker
    print(f"\n🎯 FIXED endpoint RTX 3090 utworzony!")
    print(f"🆔 ID: {endpoint_id}")
    print(f"📁 Szczegóły w: endpoint_fixed_info.json")
    print("")
    print("📋 Co dalej:")
    print("1. Active worker uruchomi się automatycznie (2-5 min)")
    print("2. Uruchom: python test_fixed_endpoint.py")
    print("3. Endpoint będzie gotowy od razu!")

if __name__ == "__main__":
    main()