# 🚀 GitHub to RunPod Deployment Guide

**Dokładna instrukcja wdrożenia FastBackend z GitHub na RunPod Serverless**

---

## 📋 **WYMAGANIA**

### ✅ **Gotowe pliki w repo:**
- `handler_fast.py` - główny handler ✅
- `handler.py` - entry point dla RunPod ✅
- `Dockerfile` - definicja obrazu Docker ✅
- `requirements.txt` - dependencies ✅
- `requirements_minimal.txt` - minimal deps ✅

### 🔧 **Konto i dostępy:**
- Konto RunPod z API key
- Repository GitHub (publiczne lub private)
- Opcjonalnie: Docker Hub account

---

## 🎯 **METODA 1: DEPLOYMENT PRZEZ RUNPOD CONSOLE (ZALECANE)**

### Krok 1: Przygotowanie Repository
```bash
# Upewnij się że masz najnowszą wersję
git pull origin master

# Sprawdź czy wszystkie pliki są commitowane
git status
```

### Krok 2: RunPod Console Setup
1. **Idź do**: https://runpod.io/console
2. **Zaloguj się** na swoje konto RunPod
3. **Przejdź do**: `Serverless` → `Endpoints`
4. **Kliknij**: `Create Endpoint`

### Krok 3: Konfiguracja Endpoint
```
🔧 KONFIGURACJA:
├── Name: "FastBackend-Matt"
├── Source: "GitHub"
├── Repository: "mateoxin/runpod-fastbackend"
├── Branch: "master"
├── Handler: "handler.handler"  # lub "handler_fast.handler"
├── Docker: Use automatic Dockerfile
└── Environment Variables: (patrz sekcja poniżej)
```

### Krok 4: Environment Variables
```bash
# WYMAGANE:
HF_TOKEN=your_huggingface_token_here
PYTHONUNBUFFERED=1

# OPCJONALNE:
WORKSPACE_PATH=/workspace
MODEL_CACHE_DIR=/workspace/models
TRAINING_DATA_PATH=/workspace/training_data
```

### Krok 5: Resource Configuration
```
📊 ZASOBY:
├── GPU Type: "NVIDIA RTX A6000" (lub RTX 4090)
├── GPU Count: 1
├── Container Disk: 50 GB
├── Volume: 100 GB (dla modeli i danych)
├── Min Workers: 0
├── Max Workers: 3
├── Idle Timeout: 5 minutes
└── Locations: EU-SE-1, US-CA-1
```

### Krok 6: Deploy
1. **Sprawdź konfigurację**
2. **Kliknij**: `Deploy`
3. **Czekaj** ~2-5 minut na deployment
4. **Sprawdź status** w Console

---

## 🎯 **METODA 2: DEPLOYMENT PRZEZ RUNPOD API**

### Krok 1: Przygotuj API Key
```bash
export RUNPOD_API_KEY="your_api_key_here"
```

### Krok 2: Deploy z API
```bash
curl -X POST https://api.runpod.ai/v2/endpoints \\
  -H "Authorization: Bearer ${RUNPOD_API_KEY}" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "FastBackend-Matt",
    "template_id": null,
    "gpu_type_id": "NVIDIA RTX A6000",
    "container_disk_in_gb": 50,
    "volume_in_gb": 100,
    "workers_min": 0,
    "workers_max": 3,
    "idle_timeout": 300,
    "locations": "EU-SE-1,US-CA-1",
    "docker_start_cmd": null,
    "env": {
      "HF_TOKEN": "your_huggingface_token_here",
      "PYTHONUNBUFFERED": "1"
    },
    "github": {
      "repo": "mateoxin/runpod-fastbackend",
      "branch": "master",
      "handler": "handler.handler"
    }
  }'
```

---

## 🎯 **METODA 3: DOCKER IMAGE DEPLOYMENT**

### Krok 1: Build Local Image
```bash
# W folderze projektu
docker build --platform linux/amd64 -t mateoxin/fastbackend:latest .
```

### Krok 2: Push do Docker Hub
```bash
docker login
docker push mateoxin/fastbackend:latest
```

### Krok 3: Deploy Image na RunPod
```bash
# W RunPod Console:
# Source: Docker Image
# Image: mateoxin/fastbackend:latest
# Handler: handler.handler
```

---

## 🧪 **TESTOWANIE DEPLOYMENT**

### Test 1: Health Check
```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"input": {"type": "health"}}'
```

**Oczekiwany wynik:**
```json
{
  "id": "job-id-12345",
  "status": "IN_QUEUE"
}
```

### Test 2: Sprawdź Status
```bash
curl -X GET https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/status/job-id-12345 \\
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Oczekiwany wynik:**
```json
{
  "status": "COMPLETED",
  "output": {
    "status": "healthy",
    "message": "Fast backend is working!",
    "environment_ready": false,
    "version": "1.0.0-fast"
  }
}
```

### Test 3: Setup Environment
```bash
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"input": {"type": "setup_environment"}}'
```

### Test 4: Upload Matt Dataset
```bash
# Ten test używa prawdziwych zdjęć z tests/10_Matt/
curl -X POST https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"input": {"type": "upload_training_data", "files": [...]}}'
```

---

## 🔧 **TESTOWANIE LOKALNE**

### Test Input (jak w dokumentacji RunPod)
```bash
python handler_fast.py --test_input '{"input": {"type": "health"}}'
```

### Local API Server (jak w dokumentacji RunPod)
```bash
# Zainstaluj dependencies
pip install fastapi uvicorn

# Uruchom local server
python handler_fast.py --rp_serve_api

# Testuj w innym terminalu
curl -X POST http://localhost:8000/run \\
  -H "Content-Type: application/json" \\
  -d '{"input": {"type": "health"}}'
```

---

## 🐛 **TROUBLESHOOTING**

### Problem 1: "Handler not found"
```bash
# Sprawdź handler path:
# Powinno być: "handler.handler" lub "handler_fast.handler"
# W RunPod Console: Endpoint → Settings → Handler
```

### Problem 2: "Import Error"
```bash
# Sprawdź requirements.txt
# Upewnij się że runpod>=1.7.0 jest w dependencies
```

### Problem 3: "Timeout podczas startup"
```bash
# Zwiększ timeout w endpoint settings
# Lub przenieś heavy setup poza handler
```

### Problem 4: "Payload too large"
```bash
# Sprawdź rozmiar requestu:
# /run: max 10MB
# /runsync: max 20MB
```

### Problem 5: "GPU Memory Error"
```bash
# Zwiększ GPU type lub container disk
# RTX A6000: 48GB VRAM
# RTX 4090: 24GB VRAM
```

---

## 📊 **MONITORING DEPLOYMENT**

### RunPod Console
```
🖥️ Console → Serverless → Your Endpoint:
├── 📈 Metrics: requests, latency, errors
├── 📋 Logs: real-time worker logs
├── ⚙️ Settings: scaling, timeouts
└── 💰 Billing: usage costs
```

### API Monitoring
```bash
# Endpoint health
curl -X GET https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/health \\
  -H "Authorization: Bearer YOUR_API_KEY"

# Worker status
curl -X GET https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/workers \\
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## ✅ **CHECKLIST PRZED DEPLOYMENT**

### Pre-deployment
- [ ] Wszystkie pliki w repo (handler_fast.py, Dockerfile, requirements.txt)
- [ ] Repository na GitHub zaktualizowane
- [ ] RunPod API key gotowy
- [ ] HuggingFace token gotowy
- [ ] GPU type wybrany

### Post-deployment
- [ ] Health check działa
- [ ] Setup environment działa
- [ ] Upload test data działa
- [ ] Logs bez błędów w Console
- [ ] Billing/costs są rozsądne

---

## 🎉 **GOTOWE!**

**Twój FastBackend będzie dostępny pod:**
```
Endpoint URL: https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run
API Key: YOUR_RUNPOD_API_KEY
```

**Do treningu LoRA z zdjęciami Matta:**
1. Upload zdjęć z `tests/10_Matt/`
2. Setup environment
3. Train z `training.yaml`
4. Download wytrenowanego modelu

**Więcej:** https://docs.runpod.io/serverless/overview