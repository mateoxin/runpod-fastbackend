# 🚀 FastBackend Deployment Guide

Kompletny przewodnik wdrożenia ultra-szybkiego backendu LoRA na RunPod.

## 📋 Spis treści

1. [Quick Start](#quick-start)
2. [Szczegółowy Setup](#szczegółowy-setup)
3. [Deployment Options](#deployment-options)
4. [Testing](#testing)
5. [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### 1-minutowy deployment:

```bash
# 1. Setup GitHub URLs
chmod +x setup_github.sh
./setup_github.sh

# 2. Deploy to RunPod
export RUNPOD_API_KEY="your_api_key"
python deploy_fast.py

# 3. Test deployment
python quick_test.py
```

## 🔧 Szczegółowy Setup

### Krok 1: Przygotowanie GitHub

1. **Sklonuj/stwórz repo:**
```bash
git clone https://github.com/mateoxin/runpod-fastbackend.git
cd YOUR_REPO/Serverless/FastBackend
```

2. **Ustaw GitHub URLs:**
```bash
export GITHUB_USERNAME="your_username"
export GITHUB_REPO="your_repo_name"
./setup_github.sh
```

3. **Wypchnij na GitHub:**
```bash
git add .
git commit -m "Add FastBackend with GitHub integration"
git push
```

### Krok 2: Konfiguracja RunPod

1. **Zdobądź API key:**
   - Idź do [RunPod Console](https://www.runpod.io/console/user/settings)
   - Skopiuj API key

2. **Ustaw zmienne środowiskowe:**
```bash
export RUNPOD_API_KEY="your_api_key"
export GITHUB_USERNAME="your_username"
export GITHUB_REPO="your_repo_name"
```

### Krok 3: Deploy

**Opcja A: Automatic Deploy**
```bash
python deploy_fast.py
# Wybierz opcję 1 (Serverless Endpoint)
```

**Opcja B: MCP Tools**
```bash
python deploy_with_mcp.py
# Użyj wygenerowanych plików JSON z MCP tools
```

**Opcja C: Manual RunPod Dashboard**
1. Stwórz nowy Pod/Endpoint
2. Image: `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04`
3. Start command: `bash -c 'curl -s https://raw.githubusercontent.com/mateoxin/runpod-fastbackend/main/Serverless/FastBackend/startup.sh | bash'`
4. Environment variables z `config.env.template`

## 🎯 Deployment Options

### 1. Serverless Endpoint (Recommended)
- ✅ Auto-scaling
- ✅ Pay per use
- ✅ Managed infrastructure
- ❌ Cold start delay

### 2. On-Demand Pod
- ✅ Consistent performance
- ✅ No cold starts
- ✅ Full control
- ❌ Pay for idle time

### 3. Spot Pod
- ✅ Cheapest option
- ✅ Good for development
- ❌ Can be interrupted
- ❌ Less reliable

## 🧪 Testing

### Local Testing
```bash
python test_local.py
```

### Endpoint Testing
```bash
# Quick test
python quick_test.py

# Specific endpoint
export RUNPOD_ENDPOINT_ID="your_endpoint_id"
python quick_test.py
```

### Load Testing
```bash
# Test with 10 concurrent requests
python quick_test.py
# Choose load test option
```

## 📊 Performance Benchmarks

| Operation | Cold Start | Warm Start | Notes |
|-----------|------------|------------|-------|
| Health Check | ~2s | ~0.1s | Instant response |
| Environment Setup | ~60-120s | ~0.1s | One-time setup |
| Training Start | ~5-10s | ~1s | After setup |
| Model List | ~1s | ~0.1s | Light operation |

## 🔄 Updates & Maintenance

### Instant Code Updates
```bash
# Edit handler_fast.py
nano handler_fast.py

# Push to GitHub
git add handler_fast.py
git commit -m "Update handler logic"
git push

# Next RunPod request uses new code automatically!
```

### Dependency Updates
```bash
# Edit requirements_minimal.txt
nano requirements_minimal.txt

# Push to GitHub
git push

# Restart RunPod pod to get new dependencies
```

### Configuration Updates
```bash
# Edit config.env
nano config.env

# Re-deploy with new config
python deploy_fast.py
```

## ❗ Troubleshooting

### Common Issues

**1. GitHub Download Failed**
```bash
# Check URLs in startup.sh
cat startup.sh | grep github.com

# Verify repo is public
curl -I https://raw.githubusercontent.com/mateoxin/runpod-fastbackend/main/Serverless/FastBackend/handler_fast.py
```

**2. Environment Setup Timeout**
```bash
# Manually trigger setup
curl -X POST "https://api.runpod.ai/v2/ENDPOINT_ID/run" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"type": "setup_environment"}}'
```

**3. PyTorch Install Failed**
- RunPod cache może być uszkodzony
- Restart pod żeby dostać świeże środowisko
- Sprawdź kompatybilność CUDA

**4. Memory Issues**
- Zmniejsz batch size w config treningu
- Użyj gradient checkpointing
- Monitoruj użycie GPU memory

### Debug Commands

**Check Environment:**
```bash
# Test health
curl -X POST "https://api.runpod.ai/v2/ENDPOINT_ID/run" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"type": "health"}}'
```

**Check Logs:**
- W RunPod dashboard: Pods → Your Pod → Logs
- Szukaj błędów setup'u i GitHub download

**Test Locally:**
```bash
python test_local.py
python handler_fast.py  # Manual test
```

## 📈 Optimization Tips

### 1. Minimize Cold Starts
- Użyj health check co 5 minut
- Keep-alive requests
- Pre-warm workers

### 2. Faster Setup
- Cache dependencies w RunPod volume
- Pre-download models
- Optimize startup script

### 3. Cost Optimization
- Użyj spot instances dla dev
- Auto-scale workers
- Monitor usage patterns

## 🔒 Security Best Practices

1. **Never commit API keys**
2. **Use environment variables**
3. **Rotate tokens regularly**
4. **Monitor access logs**
5. **Use HTTPS only**

## 📞 Support

### Jeśli coś nie działa:

1. **Check logs** w RunPod dashboard
2. **Test locally** z `python test_local.py`
3. **Verify GitHub URLs** są accessible
4. **Check API key** permissions
5. **Monitor resource usage**

### Debug Workflow:
```bash
# 1. Test local
python test_local.py

# 2. Check GitHub accessibility
curl -I https://raw.githubusercontent.com/mateoxin/runpod-fastbackend/main/Serverless/FastBackend/startup.sh

# 3. Test endpoint
python quick_test.py

# 4. Check RunPod logs
# Go to RunPod dashboard → Logs
```

---

**🎉 Happy fast deploying!**
