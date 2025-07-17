#!/usr/bin/env python3
"""
Test rapido per sistema RAG installato
Da mettere nella cartella RAG_Psicologia_Sistema e eseguire
"""

import os
import sys
from pathlib import Path
import subprocess
import time

def test_system():
    """Test completo sistema RAG installato"""
    
    print("🧠 TEST SISTEMA RAG PSICOLOGIA")
    print("=" * 40)
    
    errors = []
    
    # 1. Test directory corrente
    current_dir = Path.cwd()
    print(f"📁 Directory: {current_dir}")
    
    # 2. Test file necessari
    required_files = {
        'python/python.exe': 'Python embedded',
        'rag_system.py': 'Sistema RAG',
        'web_app.py': 'Interfaccia web', 
        'launcher.py': 'Launcher',
        '.api_key': 'API Key',
        'Rag_db': 'Database (directory)'
    }
    
    print("\n📋 VERIFICA FILE:")
    print("-" * 20)
    
    for file_path, description in required_files.items():
        path = Path(file_path)
        if path.exists():
            if path.is_file():
                size_mb = path.stat().st_size / (1024*1024)
                print(f"✅ {description}: {size_mb:.1f}MB")
            else:
                files_count = len(list(path.iterdir())) if path.is_dir() else 0
                print(f"✅ {description}: {files_count} file")
        else:
            print(f"❌ {description}: MANCANTE")
            errors.append(f"File mancante: {file_path}")
    
    # 3. Test API Key
    print("\n🔑 TEST API KEY:")
    print("-" * 15)
    
    api_file = Path('.api_key')
    if api_file.exists():
        api_key = api_file.read_text().strip()
        if api_key.startswith('sk-'):
            print(f"✅ API Key: {api_key[:10]}...{api_key[-4:]}")
        else:
            print(f"❌ API Key formato errato: {api_key[:20]}...")
            errors.append("API Key formato errato")
    else:
        print("❌ API Key: MANCANTE")
        errors.append("API Key mancante")
    
    # 4. Test Python imports
    print("\n🐍 TEST PYTHON IMPORTS:")
    print("-" * 22)
    
    python_exe = Path("python/python.exe")
    if python_exe.exists():
        test_imports = [
            "import sys; print(f'Python: {sys.version}')",
            "import openai; print('✅ OpenAI')",
            "import chromadb; print('✅ ChromaDB')", 
            "import streamlit; print('✅ Streamlit')",
            "import fitz; print('✅ PyMuPDF')",
            "from pathlib import Path; print(f'Database: {len(list(Path(\"Rag_db\").iterdir()))} file')"
        ]
        
        for test_cmd in test_imports:
            try:
                result = subprocess.run([
                    str(python_exe), "-c", test_cmd
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(result.stdout.strip())
                else:
                    print(f"❌ Errore: {result.stderr.strip()}")
                    errors.append(f"Import fallito: {test_cmd}")
                    
            except subprocess.TimeoutExpired:
                print("⏰ Timeout import")
                errors.append(f"Timeout: {test_cmd}")
            except Exception as e:
                print(f"❌ Errore esecuzione: {e}")
                errors.append(f"Errore Python: {e}")
    else:
        print("❌ Python non trovato")
        errors.append("Python embedded non trovato")
    
    # 5. Test Database ChromaDB
    print("\n🗄️ TEST DATABASE:")
    print("-" * 16)
    
    if python_exe.exists():
        db_test = '''
import chromadb
from pathlib import Path

try:
    client = chromadb.PersistentClient(path="./Rag_db")
    collections = client.list_collections()
    print(f"✅ ChromaDB: {len(collections)} collezioni")
    
    for collection in collections:
        count = collection.count()
        print(f"  - {collection.name}: {count} documenti")
        
except Exception as e:
    print(f"❌ Errore database: {e}")
'''
        
        try:
            result = subprocess.run([
                str(python_exe), "-c", db_test
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                print(result.stdout.strip())
            else:
                print(f"❌ Errore database: {result.stderr.strip()}")
                errors.append("Test database fallito")
                
        except Exception as e:
            print(f"❌ Errore test database: {e}")
            errors.append(f"Errore test database: {e}")
    
    # 6. Test launcher
    print("\n🚀 TEST LAUNCHER:")
    print("-" * 15)
    
    launcher_file = Path("launcher.py")
    if launcher_file.exists():
        print("✅ Launcher disponibile")
        print("💡 Per avviare sistema: python python/python.exe launcher.py")
    else:
        print("❌ Launcher mancante")
        errors.append("Launcher mancante")
    
    # 7. Risultato finale
    print("\n" + "=" * 40)
    
    if not errors:
        print("🎉 SISTEMA RAG: COMPLETAMENTE FUNZIONANTE!")
        print("\n🚀 Per avviare:")
        print("   1. Doppio-click su 'AVVIA_RAG_PSICOLOGIA.bat'")
        print("   2. Oppure: python python/python.exe launcher.py")
        print("\n🌐 Interfaccia: http://localhost:8501")
    else:
        print("❌ PROBLEMI RILEVATI:")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
        
        print("\n💡 RACCOMANDAZIONI:")
        if "API Key" in str(errors):
            print("   - Verifica file .api_key con chiave corretta")
        if "Python" in str(errors):
            print("   - Reinstalla sistema completo")
        if "Database" in str(errors):
            print("   - Verifica che Rag_db sia stato copiato correttamente")
    
    return len(errors) == 0

if __name__ == "__main__":
    try:
        success = test_system()
        print(f"\n🏁 Test completato: {'SUCCESSO' if success else 'ERRORI'}")
    except KeyboardInterrupt:
        print("\n⏹️ Test interrotto")
    except Exception as e:
        print(f"\n💥 Errore test: {e}")
    
    input("\nPremi Invio per uscire...")