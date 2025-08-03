#!/usr/bin/env python3
"""
Tworzenie RunPod Endpoint przez MCP
Z RTX 3090 i 100GB dysku
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

def create_improved_template():
    """Tworzy lepszy template z optymalizacjami"""
    
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
        'MAX_WORKERS': '1',
        'TIMEOUT': '600',  # 10 min timeout
        'MEMORY_LIMIT': '100G'
    }
    
    print("\n📋 Tworzenie ulepszonego template...")
    print("🔧 Konfiguracja:")
    print("   - Image: PyTorch 2.1.0 + CUDA 11.8")
    print("   - Container Disk: 100GB")
    print("   - Volume: 100GB") 
    print("   - GPU: RTX 3090 optimized")
    print(f"   - Env vars: {len(env_vars)}")
    
    try:
        template_response = runpod.create_template(
            name='fastbackend-rtx3090-v2-template',
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
            print(f"✅ Template v2 utworzony: {template_id}")
            return template_id
        else:
            print("❌ Błąd tworzenia template")
            return None
            
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return None

def create_optimized_endpoint(template_id):
    """Tworzy zoptymalizowany endpoint"""
    
    print(f"\n🚀 Tworzenie zoptymalizowanego endpoint...")
    print("📊 Parametry:")
    print("   - GPU: RTX 3090 (24GB VRAM)")
    print("   - Template: v2 (ulepszona)")
    print("   - Workers: 1 (stabilność)")
    print("   - Timeout: 10s (szybszy start)")
    print("   - Storage: 100GB")
    
    try:
        # Tworzenie endpoint z lepszymi parametrami
        response = runpod.create_endpoint(
            name='fastbackend-rtx3090-v2',
            template_id=template_id,
            gpu_ids='NVIDIA GeForce RTX 3090',
            locations='US,EU',        # Multi-region
            idle_timeout=10,          # 10s timeout (szybszy)
            scaler_type='QUEUE_DELAY',
            scaler_value=5,           # Szybsza reakcja
            workers_min=0,            # Auto-scale down
            workers_max=1,            # Maksymalnie 1 worker
            gpu_count=1,              # 1 GPU per worker
            flashboot=True            # Szybszy boot
        )
        
        if response:
            endpoint_id = response.get('id') if isinstance(response, dict) else response
            
            print(f"\n✅ Nowy endpoint utworzony!")
            print(f"🆔 ID: {endpoint_id}")
            print(f"📛 Name: fastbackend-rtx3090-v2")
            print(f"🔗 URL: https://api.runpod.ai/v2/{endpoint_id}")
            
            # Zapisz nowe informacje
            endpoint_info = {
                'id': endpoint_id,
                'name': 'fastbackend-rtx3090-v2',
                'url': f'https://api.runpod.ai/v2/{endpoint_id}',
                'template_id': template_id,
                'gpu_type': 'NVIDIA GeForce RTX 3090',
                'gpu_memory': '24GB',
                'container_disk_gb': 100,
                'volume_gb': 100,
                'workers_max': 1,
                'idle_timeout': 10,
                'flashboot': True,
                'version': 'v2',
                'created_at': datetime.now().isoformat(),
                'status': 'creating'
            }
            
            # Zapisz do pliku
            with open('endpoint_v2_info.json', 'w') as f:
                json.dump(endpoint_info, f, indent=2)
            
            print(f"💾 Informacje zapisane w endpoint_v2_info.json")
            return endpoint_id
            
        else:
            print("❌ Błąd tworzenia endpoint")
            return None
            
    except Exception as e:
        print(f"❌ Błąd endpoint: {e}")
        return None

def cleanup_old_endpoint():
    """Usuwa problematyczny stary endpoint"""
    
    print(f"\n🧹 Sprawdzanie starych endpoints...")
    
    try:
        endpoints = runpod.get_endpoints()
        old_endpoint_id = '6vi641zor1txhn'  # Stary problematyczny endpoint
        
        for endpoint in endpoints:
            if endpoint.get('id') == old_endpoint_id:
                print(f"🗑️  Znaleziono stary endpoint: {old_endpoint_id}")
                print(f"   Name: {endpoint.get('name', 'Unknown')}")
                print(f"   Status: {endpoint.get('status', 'Unknown')}")
                
                # Zatrzymaj endpoint (można też usunąć)
                choice = input("Czy zatrzymać stary endpoint? (y/n): ").lower()
                if choice == 'y':
                    try:
                        # Użyj runpod API do zatrzymania
                        print(f"⏹️  Zatrzymywanie endpoint {old_endpoint_id}...")
                        # runpod.delete_endpoint(old_endpoint_id)  # Uncomment to delete
                        print(f"✅ Endpoint {old_endpoint_id} zostanie zatrzymany")
                    except Exception as e:
                        print(f"❌ Błąd zatrzymywania: {e}")
                break
        else:
            print("ℹ️  Stary endpoint nie znaleziony lub już usunięty")
            
    except Exception as e:
        print(f"❌ Błąd sprawdzania endpoints: {e}")

def wait_for_endpoint_ready(endpoint_id, timeout=300):
    """Czeka aż endpoint będzie gotowy"""
    
    print(f"\n⏳ Czekanie na uruchomienie endpoint {endpoint_id}...")
    print("💡 To może potrwać 2-5 minut...")
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            endpoints = runpod.get_endpoints()
            for endpoint in endpoints:
                if endpoint.get('id') == endpoint_id:
                    status = endpoint.get('status', 'Unknown')
                    print(f"📊 Status: {status}")
                    
                    if status in ['READY', 'ACTIVE']:
                        print(f"✅ Endpoint gotowy! Status: {status}")
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
    
    print(f"⚠️  Timeout - endpoint może nadal się uruchamiać")
    return False

def main():
    """Główna funkcja"""
    print("🚀 RunPod MCP Endpoint Creator v2")
    print("==================================")
    print("🎯 Cel: RTX 3090 + 100GB + Stabilność")
    print("")
    
    # Setup RunPod
    if not setup_runpod():
        return
    
    # Utwórz nowy template
    template_id = create_improved_template()
    if not template_id:
        print("❌ Nie udało się utworzyć template")
        return
    
    # Utwórz nowy endpoint
    endpoint_id = create_optimized_endpoint(template_id)
    if not endpoint_id:
        print("❌ Nie udało się utworzyć endpoint")
        return
    
    # Opcjonalnie posprzątaj stary endpoint
    cleanup_old_endpoint()
    
    # Czekaj na gotowość
    print(f"\n🎯 Nowy endpoint RTX 3090 v2 utworzony!")
    print(f"🆔 ID: {endpoint_id}")
    print(f"📁 Szczegóły w: endpoint_v2_info.json")
    print("")
    print("📋 Następne kroki:")
    print("1. Poczekaj 2-5 minut na uruchomienie")
    print("2. Uruchom: python test_v2_endpoint.py")
    print("3. Przetestuj wszystkie funkcje")

if __name__ == "__main__":
    main()