#!/bin/bash

echo "🔧 Konfiguracja środowiska RunPod FastBackend"
echo "=============================================="

# Aktywacja wirtualnego środowiska Python
if [ -d "venv" ]; then
    echo "✅ Aktywacja wirtualnego środowiska Python..."
    source venv/bin/activate
else
    echo "❌ Nie znaleziono venv/ - uruchom najpierw instalację"
    exit 1
fi

# Ładowanie tokenów
if [ -f "config.env" ]; then
    echo "🔑 Ładowanie tokenów z config.env..."
    export $(grep -v '^#' config.env | xargs)
    echo "✅ Tokeny załadowane:"
    echo "  - RunPod API Key: ${RUNPOD_API_KEY:0:10}..."
    echo "  - HF Token: ${HF_TOKEN:0:10}..."
    echo "  - GitHub Token: ${GITHUB_TOKEN:0:10}..."
    echo "  - Smithery Token: ${SMITHERY_TOKEN:0:10}..."
else
    echo "❌ Nie znaleziono config.env"
    exit 1
fi

# Konfiguracja Node.js/nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

echo ""
echo "🚀 Środowisko gotowe!"
echo "📋 Dostępne komendy:"
echo "  - python tests/simple_test.py           # Podstawowy test"
echo "  - python tests/test_with_matt_dataset.py # Test z danymi Matt"
echo "  - python tests/run_all_tests.py         # Pełna seria testów"
echo ""
echo "🔧 MCP RunPod zostało zainstalowane w Cursor"
echo "   Tokeny są gotowe do użycia w testach!"