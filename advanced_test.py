#!/usr/bin/env python3
"""
Test Avanzato Sistema RAG - Verifica completa post-installazione
Compatibile con il nuovo installer robusto
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import json

class AdvancedRAGTester:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.errors = []
        self.warnings = []
        self.test_results = {}
        
    def print_header(self, title, char="="):
        """Stampa header formattato"""
        print(f"\n{char * 60}")
        print(f"🧠 {title}")
        print(f"{char * 60}")
    
    def log_result(self, test_name, status, message="", details=None):
        """Log risultato test"""
        self.test_results[test_name] = {
            'status': status,
            'message': message,
            'details': details
        }
        
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{icon} {test_name}: {message}")
        
        if details:
            for detail in details:
                print(f"   • {detail}")
    
    def test_directory_structure(self):
        """Test 1: Struttura directory"""
        self.print_header("TEST 1: STRUTTURA DIRECTORY")
        
        required_structure = {
            'python/python.exe': 'Python Embedded Executable',
            'python/Scripts/': 'Scripts Python (opzionale)',
            'rag_system.py': 'Sistema RAG Core',
            'web_app.py': 'Interfaccia Web Streamlit',
            'launcher.py': 'Launcher Sistema',
            '.api_key': 'File API Key OpenAI',
            'Rag_db/': 'Database ChromaDB',
            '🚀 AVVIA_RAG_PSICOLOGIA.bat': 'Launcher Windows',
            'README_UTENTE.txt': 'Documentazione Utente'
        }
        
        missing_files = []
        present_files = []
        
        for file_path, description in required_structure.items():
            path = Path(file_path)
            if path.exists():
                if path.is_file():
                    size_mb = path.stat().st_size / (1024*1024)
                    present_files.append(f"{description}: {size_mb:.2f}MB")
                else:
                    file_count = len(list(path.iterdir())) if path.is_dir() else 0
                    present_files.append(f"{description}: {file_count} elementi")
            else:
                missing_files.append(f"{description} ({file_path})")
        
        if not missing_files:
            self.log_result("Struttura Directory", "PASS", "Tutti i file richiesti presenti", present_files)
        else:
            self.log_result("Struttura Directory", "FAIL", f"{len(missing_files)} file mancanti", missing_files)
            self.errors.extend(missing_files)
    
    def test_python_environment(self):
        """Test 2: Ambiente Python"""
        self.print_header("TEST 2: AMBIENTE PYTHON")
        
        python_exe = Path("python/python.exe")
        
        if not python_exe.exists():
            self.log_result("Python Executable", "FAIL", "python.exe non trovato")
            self.errors.append("Python embedded non installato")
            return
        
        # Test versione Python
        try:
            result = subprocess.run([
                str(python_exe), "--version"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                python_version = result.stdout.strip()
                self.log_result("Python Version", "PASS", python_version)
            else:
                self.log_result("Python Version", "FAIL", "Impossibile ottenere versione")
                self.errors.append("Python version check failed")
        
        except subprocess.TimeoutExpired:
            self.log_result("Python Version", "FAIL", "Timeout durante verifica versione")
            self.errors.append("Python timeout")
        except Exception as e:
            self.log_result("Python Version", "FAIL", f"Errore: {str(e)}")
            self.errors.append(f"Python error: {str(e)}")
    
    def test_python_packages(self):
        """Test 3: Pacchetti Python"""
        self.print_header("TEST 3: PACCHETTI PYTHON")
        
        python_exe = Path("python/python.exe")
        
        if not python_exe.exists():
            self.log_result("Package Test", "SKIP", "Python non disponibile")
            return
        
        # Pacchetti essenziali
        essential_packages = {
            'openai': 'OpenAI API Client',
            'chromadb': 'ChromaDB Vector Database',
            'streamlit': 'Streamlit Web Framework'
        }
        
        # Pacchetti opzionali
        optional_packages = {
            'PyMuPDF': 'PDF Processing (fitz)',
            'Pillow': 'Image Processing',
            'nltk': 'Natural Language Toolkit'
        }
        
        installed_essential = []
        missing_essential = []
        installed_optional = []
        missing_optional = []
        
        def test_package_group(packages, installed_list, missing_list):
            for package, description in packages.items():
                try:
                    result = subprocess.run([
                        str(python_exe), "-c", f"import {package.lower()}; print(f'{package}: OK')"
                    ], capture_output=True, text=True, timeout=15)
                    
                    if result.returncode == 0:
                        # Prova a ottenere versione
                        try:
                            version_result = subprocess.run([
                                str(python_exe), "-c", 
                                f"import {package.lower()}; print(getattr({package.lower()}, '__version__', 'N/A'))"
                            ], capture_output=True, text=True, timeout=10)
                            
                            version = version_result.stdout.strip() if version_result.returncode == 0 else "N/A"
                            installed_list.append(f"{description}: v{version}")
                        except:
                            installed_list.append(f"{description}: OK")
                    else:
                        missing_list.append(f"{description} ({package})")
                
                except subprocess.TimeoutExpired:
                    missing_list.append(f"{description} ({package}) - Timeout")
                except Exception as e:
                    missing_list.append(f"{description} ({package}) - Error: {str(e)}")
        
        # Test pacchetti essenziali
        test_package_group(essential_packages, installed_essential, missing_essential)
        
        # Test pacchetti opzionali
        test_package_group(optional_packages, installed_optional, missing_optional)
        
        # Risultati pacchetti essenziali
        if not missing_essential:
            self.log_result("Pacchetti Essenziali", "PASS", f"{len(installed_essential)} pacchetti OK", installed_essential)
        else:
            self.log_result("Pacchetti Essenziali", "FAIL", f"{len(missing_essential)} pacchetti mancanti", missing_essential)
            self.errors.extend(missing_essential)
        
        # Risultati pacchetti opzionali
        if not missing_optional:
            self.log_result("Pacchetti Opzionali", "PASS", f"{len(installed_optional)} pacchetti OK", installed_optional)
        elif len(installed_optional) > 0:
            self.log_result("Pacchetti Opzionali", "WARNING", f"{len(missing_optional)} mancanti, {len(installed_optional)} OK", 
                          installed_optional + [f"MANCANTI: {', '.join(missing_optional)}"])
            self.warnings.extend(missing_optional)
        else:
            self.log_result("Pacchetti Opzionali", "FAIL", "Tutti i pacchetti opzionali mancanti", missing_optional)
            self.warnings.extend(missing_optional)
    
    def test_api_key(self):
        """Test 4: API Key OpenAI"""
        self.print_header("TEST 4: API KEY OPENAI")
        
        api_file = Path('.api_key')
        
        if not api_file.exists():
            self.log_result("API Key File", "FAIL", "File .api_key non trovato")
            self.errors.append("API Key file missing")
            return
        
        try:
            api_key = api_file.read_text().strip()
            
            if not api_key:
                self.log_result("API Key Content", "FAIL", "File API key vuoto")
                self.errors.append("Empty API key")
            elif not api_key.startswith('sk-'):
                self.log_result("API Key Format", "FAIL", "Formato API key errato (deve iniziare con 'sk-')")
                self.errors.append("Invalid API key format")
            elif len(api_key) < 45:
                self.log_result("API Key Length", "WARNING", "API key sembra troppo corta")
                self.warnings.append("Short API key")
            else:
                masked_key = f"{api_key[:10]}...{api_key[-4:]}"
                self.log_result("API Key", "PASS", f"Formato valido: {masked_key}")
        
        except Exception as e:
            self.log_result("API Key", "FAIL", f"Errore lettura: {str(e)}")
            self.errors.append(f"API key read error: {str(e)}")
    
    def test_database(self):
        """Test 5: Database ChromaDB"""
        self.print_header("TEST 5: DATABASE CHROMADB")
        
        python_exe = Path("python/python.exe")
        db_path = Path("Rag_db")
        
        if not db_path.exists():
            self.log_result("Database Directory", "FAIL", "Cartella Rag_db non trovata")
            self.errors.append("Database directory missing")
            return
        
        # Conta file database
        all_files = list(db_path.rglob('*'))
        db_files = [f for f in all_files if f.is_file()]
        
        if len(db_files) == 0:
            self.log_result("Database Files", "FAIL", "Nessun file nel database")
            self.errors.append("Empty database")
            return
        
        self.log_result("Database Files", "PASS", f"{len(db_files)} file trovati")
        
        # Test accesso ChromaDB
        if not python_exe.exists():
            self.log_result("Database Access", "SKIP", "Python non disponibile per test accesso")
            return
        
        db_test_script = '''
import chromadb
from pathlib import Path
import json

try:
    client = chromadb.PersistentClient(path="./Rag_db")
    collections = client.list_collections()
    
    result = {
        "collections_count": len(collections),
        "collections": []
    }
    
    for collection in collections:
        try:
            count = collection.count()
            result["collections"].append({
                "name": collection.name,
                "documents": count
            })
        except Exception as e:
            result["collections"].append({
                "name": collection.name,
                "error": str(e)
            })
    
    print("SUCCESS:" + json.dumps(result))
    
except Exception as e:
    print(f"ERROR:{str(e)}")
'''
        
        try:
            result = subprocess.run([
                str(python_exe), "-c", db_test_script
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and "SUCCESS:" in result.stdout:
                # Parsing risultato
                json_str = result.stdout.split("SUCCESS:")[1].strip()
                db_info = json.loads(json_str)
                
                details = [f"Collezioni: {db_info['collections_count']}"]
                total_docs = 0
                
                for col in db_info['collections']:
                    if 'documents' in col:
                        details.append(f"  • {col['name']}: {col['documents']} documenti")
                        total_docs += col['documents']
                    else:
                        details.append(f"  • {col['name']}: ERRORE - {col.get('error', 'Unknown')}")
                
                if total_docs > 0:
                    self.log_result("Database Access", "PASS", f"{total_docs} documenti totali", details)
                else:
                    self.log_result("Database Access", "WARNING", "Database vuoto", details)
                    self.warnings.append("Empty database collections")
                    
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                self.log_result("Database Access", "FAIL", f"Errore accesso database: {error_msg}")
                self.errors.append(f"Database access error: {error_msg}")
                
        except subprocess.TimeoutExpired:
            self.log_result("Database Access", "FAIL", "Timeout test database")
            self.errors.append("Database test timeout")
        except Exception as e:
            self.log_result("Database Access", "FAIL", f"Errore test: {str(e)}")
            self.errors.append(f"Database test error: {str(e)}")
    
    def test_system_integration(self):
        """Test 6: Integrazione Sistema"""
        self.print_header("TEST 6: INTEGRAZIONE SISTEMA")
        
        python_exe = Path("python/python.exe")
        
        if not python_exe.exists():
            self.log_result("System Integration", "SKIP", "Python non disponibile")
            return
        
        # Test import completo del sistema
        integration_test = '''
import os
import sys
from pathlib import Path

# Imposta API key se disponibile
try:
    with open('.api_key', 'r') as f:
        api_key = f.read().strip()
    os.environ['OPENAI_API_KEY'] = api_key
except:
    pass

try:
    # Test import sistema RAG
    from rag_system import SimpleRAGQuery
    print("✅ RAG System import OK")
    
    # Test inizializzazione (senza chiamate API)
    if os.getenv('OPENAI_API_KEY'):
        rag = SimpleRAGQuery(os.getenv('OPENAI_API_KEY'), db_path="./Rag_db")
        print("✅ RAG System initialization OK")
    else:
        print("⚠️ API key non trovata, skip inizializzazione")
    
    # Test import web app
    import streamlit
    print("✅ Streamlit import OK")
    
    print("SUCCESS: Sistema integrato correttamente")
    
except ImportError as e:
    print(f"IMPORT_ERROR: {str(e)}")
except Exception as e:
    print(f"ERROR: {str(e)}")
'''
        
        try:
            result = subprocess.run([
                str(python_exe), "-c", integration_test
            ], capture_output=True, text=True, timeout=45)
            
            if result.returncode == 0 and "SUCCESS:" in result.stdout:
                # Estrai dettagli
                lines = result.stdout.strip().split('\n')
                success_details = [line for line in lines if line.startswith('✅') or line.startswith('⚠️')]
                
                self.log_result("System Integration", "PASS", "Tutti i componenti integrati", success_details)
                
            elif "IMPORT_ERROR:" in result.stdout:
                error_msg = result.stdout.split("IMPORT_ERROR:")[1].strip()
                self.log_result("System Integration", "FAIL", f"Errore import: {error_msg}")
                self.errors.append(f"Integration import error: {error_msg}")
                
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                self.log_result("System Integration", "FAIL", f"Errore integrazione: {error_msg}")
                self.errors.append(f"Integration error: {error_msg}")
                
        except subprocess.TimeoutExpired:
            self.log_result("System Integration", "FAIL", "Timeout test integrazione")
            self.errors.append("Integration test timeout")
        except Exception as e:
            self.log_result("System Integration", "FAIL", f"Errore test: {str(e)}")
            self.errors.append(f"Integration test error: {str(e)}")
    
    def test_launcher_functionality(self):
        """Test 7: Funzionalità Launcher"""
        self.print_header("TEST 7: FUNZIONALITÀ LAUNCHER")
        
        launcher_bat = Path("🚀 AVVIA_RAG_PSICOLOGIA.bat")
        launcher_py = Path("launcher.py")
        
        # Test esistenza launcher
        if not launcher_bat.exists():
            self.log_result("Launcher BAT", "FAIL", "File launcher .bat non trovato")
            self.errors.append("BAT launcher missing")
        else:
            content = launcher_bat.read_text(encoding='utf-8')
            if "python\\python.exe launcher.py" in content:
                self.log_result("Launcher BAT", "PASS", "Launcher .bat configurato correttamente")
            else:
                self.log_result("Launcher BAT", "WARNING", "Contenuto launcher .bat sospetto")
                self.warnings.append("BAT launcher content")
        
        if not launcher_py.exists():
            self.log_result("Launcher Python", "FAIL", "File launcher.py non trovato")
            self.errors.append("Python launcher missing")
            return
        
        # Test sintassi launcher Python
        python_exe = Path("python/python.exe")
        if python_exe.exists():
            try:
                result = subprocess.run([
                    str(python_exe), "-m", "py_compile", "launcher.py"
                ], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    self.log_result("Launcher Syntax", "PASS", "Sintassi launcher.py corretta")
                else:
                    self.log_result("Launcher Syntax", "FAIL", f"Errore sintassi: {result.stderr}")
                    self.errors.append(f"Launcher syntax error: {result.stderr}")
                    
            except Exception as e:
                self.log_result("Launcher Syntax", "WARNING", f"Impossibile testare sintassi: {str(e)}")
                self.warnings.append(f"Launcher syntax test error: {str(e)}")
        else:
            self.log_result("Launcher Syntax", "SKIP", "Python non disponibile")
    
    def generate_summary(self):
        """Genera riassunto finale"""
        self.print_header("RIASSUNTO FINALE", "=")
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results.values() if t['status'] == 'PASS'])
        failed_tests = len([t for t in self.test_results.values() if t['status'] == 'FAIL'])
        warning_tests = len([t for t in self.test_results.values() if t['status'] == 'WARNING'])
        skipped_tests = len([t for t in self.test_results.values() if t['status'] == 'SKIP'])
        
        print(f"\n📊 RISULTATI TEST:")
        print(f"   ✅ Passati: {passed_tests}/{total_tests}")
        print(f"   ❌ Falliti: {failed_tests}")
        print(f"   ⚠️ Warning: {warning_tests}")
        print(f"   ⏭️ Saltati: {skipped_tests}")
        
        # Status finale
        if failed_tests == 0 and len(self.errors) == 0:
            print(f"\n🎉 SISTEMA RAG: COMPLETAMENTE FUNZIONANTE!")
            print(f"✅ Tutti i test critici superati")
            
            if warning_tests > 0:
                print(f"\n⚠️ Note ({warning_tests} warning):")
                for warning in self.warnings:
                    print(f"   • {warning}")
            
            print(f"\n🚀 ISTRUZIONI AVVIO:")
            print(f"   1. Doppio-click su '🚀 AVVIA_RAG_PSICOLOGIA.bat'")
            print(f"   2. Attendi apertura browser automatica")
            print(f"   3. Interfaccia disponibile su: http://localhost:8501")
            
        else:
            print(f"\n❌ PROBLEMI RILEVATI ({len(self.errors)} errori critici):")
            for i, error in enumerate(self.errors, 1):
                print(f"   {i}. {error}")
            
            print(f"\n💡 RACCOMANDAZIONI:")
            if any("API Key" in error for error in self.errors):
                print(f"   🔑 Verifica configurazione API Key OpenAI")
            if any("Python" in error for error in self.errors):
                print(f"   🐍 Reinstalla sistema Python embedded")
            if any("Database" in error for error in self.errors):
                print(f"   🗄️ Verifica integrità database Rag_db")
            if any("package" in error.lower() for error in self.errors):
                print(f"   📦 Reinstalla dipendenze Python")
        
        # Informazioni sistema
        print(f"\n📁 DIRECTORY SISTEMA: {self.current_dir}")
        
        return len(self.errors) == 0
    
    def run_all_tests(self):
        """Esegue tutti i test"""
        self.print_header("TEST SISTEMA RAG PSICOLOGIA", "=")
        
        print(f"📁 Directory di test: {self.current_dir}")
        print(f"🕐 Inizio test: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Esegui tutti i test
        test_methods = [
            self.test_directory_structure,
            self.test_python_environment,
            self.test_python_packages,
            self.test_api_key,
            self.test_database,
            self.test_system_integration,
            self.test_launcher_functionality
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                test_name = test_method.__name__.replace('test_', '').replace('_', ' ').title()
                self.log_result(test_name, "FAIL", f"Errore durante test: {str(e)}")
                self.errors.append(f"{test_name}: {str(e)}")
        
        # Genera riassunto
        success = self.generate_summary()
        
        print(f"\n🏁 Test completati: {'SUCCESSO' if success else 'ERRORI RILEVATI'}")
        print(f"🕐 Fine test: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return success

def main():
    """Funzione principale"""
    try:
        tester = AdvancedRAGTester()
        success = tester.run_all_tests()
        
        exit_code = 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrotti dall'utente")
        exit_code = 2
    except Exception as e:
        print(f"\n\n💥 Errore critico durante test: {str(e)}")
        exit_code = 3
    
    print(f"\n{'='*60}")
    input("Premi Invio per uscire...")
    return exit_code

if __name__ == "__main__":
    sys.exit(main())