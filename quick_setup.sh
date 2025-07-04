#!/bin/bash

echo "🚀 Creando struttura progetto RAG..."

# Crea directory GitHub Actions
mkdir -p .github/workflows

# 1. requirements.txt
cat > requirements.txt << 'EOF'
pyinstaller>=5.0.0
Pillow>=10.0.0
EOF

# 2. GitHub workflow
cat > .github/workflows/build.yml << 'EOF'
name: Compila EXE

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - name: Scarica codice
      uses: actions/checkout@v4
    
    - name: Setup Python  
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Installa dipendenze
      run: |
        pip install pyinstaller Pillow
    
    - name: Compila EXE
      run: |
        pyinstaller --onefile --windowed --name "RAG_Psicologia_Installer" smart_installer.py
    
    - name: Upload EXE
      uses: actions/upload-artifact@v3
      with:
        name: RAG-Installer-EXE
        path: dist/RAG_Psicologia_Installer.exe
EOF

# 3. README.md
cat > README.md << 'EOF'
# 🧠 Sistema RAG Psicologia - Installer

Sistema di consultazione intelligente per documenti di psicologia.

## 🚀 Build Automatica

Ogni push triggera la compilazione dell'installer Windows.

## 📥 Download EXE

1. Vai su **Actions** 
2. Click sull'ultimo build
3. Scarica **RAG-Installer-EXE** 

## 📦 Uso

Distribuire `RAG_Psicologia_Installer.exe` con cartella `Rag_db/`.
EOF

# 4. .gitignore
cat > .gitignore << 'EOF'
# Build
dist/
build/
*.spec

# Python  
__pycache__/
*.pyc

# Local
.env
.api_key
.DS_Store
EOF

# 5. Istruzioni utente
cat > ISTRUZIONI_UTENTE.txt << 'EOF'
🧠 SISTEMA RAG PSICOLOGIA - GUIDA RAPIDA
========================================

⚠️ IMPORTANTE: PRIMA DI INIZIARE
================================
Assicurati di avere ENTRAMBI nella stessa cartella:
✅ RAG_Psicologia_Installer.exe
✅ Cartella "Rag_db" (contiene il database dei documenti)

🚀 INSTALLAZIONE:
================
1. Doppio-click su RAG_Psicologia_Installer.exe  
2. Inserisci API Key OpenAI (inizia con "sk-")
3. L'installer controllerà automaticamente la presenza di Rag_db
4. Aspetta installazione automatica (5-10 min)
5. Si aprirà il browser automaticamente

🔍 ESEMPI DOMANDE:
==================
- "Qual è la differenza tra ansia e angoscia?"
- "Come viene definito il transfert?"
- "Caratteristiche del disturbo borderline?"

🚀 AVVIO FUTURO:
===============
Dopo installazione, per usare il sistema:
Doppio-click su "🚀 AVVIA_RAG_PSICOLOGIA.bat"

📁 STRUTTURA DISTRIBUZIONE:
===========================
📦 Pacchetto_RAG_Psicologia/
├── RAG_Psicologia_Installer.exe  ← Installer 
├── Rag_db/                       ← Database (ESSENZIALE!)
│   ├── [file database...]
└── ISTRUZIONI_UTENTE.txt         ← Questo file

💡 PROBLEMI COMUNI:
==================
❌ "Database RAG non trovato"
   → Verifica che cartella Rag_db sia nella stessa directory dell'installer

❌ "Errore API Key"  
   → Verifica che inizi con "sk-" e sia quella fornita

❌ Connessione internet necessaria solo per installazione
EOF

echo "✅ File base creati!"
echo ""
echo "📝 PROSSIMO STEP:"
echo "Devi copiare questi 3 file dei tuoi script esistenti:"
echo "- smart_installer.py"  
echo "- rag_system.py"
echo "- web_app.py"
echo ""
echo "💡 DOVE SONO I TUOI FILE?"
echo ""
echo "🔍 Controllo file esistenti..."

# Controlla quali file Python esistono già
if [ -f "smart_installer.py" ]; then
    echo "✅ smart_installer.py trovato"
else
    echo "❌ smart_installer.py manca"
fi

if [ -f "rag_system.py" ]; then
    echo "✅ rag_system.py trovato"
else
    echo "❌ rag_system.py manca"
fi

if [ -f "web_app.py" ]; then
    echo "✅ web_app.py trovato"
else
    echo "❌ web_app.py manca"
fi

echo ""
echo "📂 Contenuto cartella attuale:"
ls -la