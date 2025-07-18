#!/usr/bin/env python3
"""
Smart Installer RAG - Versione CORRETTA
Fixes: source_db_path, launcher string escaping, database path mapping
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import shutil
import zipfile
import urllib.request

class SimpleRAGInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧠 RAG Psicologia - Setup Automatico")
        self.root.geometry("600x550")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(True, True)
        
        # Configurazione
        self.python_version = "3.11.8"
        self.install_dir = Path.cwd() / "RAG_Psicologia_Sistema"
        self.python_embedded_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-embed-amd64.zip"
        
        # Variabili - FIX: Inizializza source_db_path
        self.api_key = ""
        self.setup_complete = False
        self.source_db_path = None  # FIX: Aggiunti inizializzazione
        
        self.create_interface()
    
    def create_interface(self):
        """Interfaccia semplice"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#1e3a8a', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🧠 Sistema RAG Psicologia",
            font=("Arial", 18, "bold"),
            fg="white",
            bg='#1e3a8a'
        )
        title_label.pack(expand=True)
        
        # Contenuto principale
        main_frame = tk.Frame(self.root, bg='#f0f8ff', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Directory installazione
        tk.Label(
            main_frame,
            text="📁 Directory installazione:",
            font=("Arial", 10, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w')
        
        dir_frame = tk.Frame(main_frame, bg='#f0f8ff')
        dir_frame.pack(fill='x', pady=5)
        
        self.dir_var = tk.StringVar(value=str(self.install_dir))
        dir_entry = tk.Entry(dir_frame, textvariable=self.dir_var, font=("Arial", 10), width=50)
        dir_entry.pack(side='left', fill='x', expand=True)
        
        tk.Button(dir_frame, text="📂", command=self.choose_directory, width=3).pack(side='right', padx=(5, 0))
        
        # Database path
        tk.Label(
            main_frame,
            text="🗄️ Database Rag_db:",
            font=("Arial", 10, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w', pady=(15, 0))
        
        db_frame = tk.Frame(main_frame, bg='#f0f8ff')
        db_frame.pack(fill='x', pady=5)
        
        default_db = Path.cwd() / "Rag_db"
        self.db_var = tk.StringVar(value=str(default_db))
        db_entry = tk.Entry(db_frame, textvariable=self.db_var, font=("Arial", 10), width=50)
        db_entry.pack(side='left', fill='x', expand=True)
        
        tk.Button(db_frame, text="📂", command=self.choose_database, width=3).pack(side='right', padx=(5, 0))
        
        # Auto-detect button
        tk.Button(
            main_frame,
            text="🔍 Auto-rileva Rag_db",
            command=self.auto_detect_database,
            bg='#6366f1',
            fg='white',
            font=("Arial", 9)
        ).pack(pady=5)
        
        # Test database button
        tk.Button(
            main_frame,
            text="✅ Testa Database",
            command=self.test_database,
            bg='#10b981',
            fg='white',
            font=("Arial", 9)
        ).pack(pady=5)
        
        # API Key
        tk.Label(
            main_frame,
            text="🔑 OpenAI API Key:",
            font=("Arial", 11, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w', pady=(15, 0))
        
        self.api_entry = tk.Entry(
            main_frame,
            font=("Arial", 11),
            width=50,
            show="*"
        )
        self.api_entry.pack(fill='x', pady=5)
        
        # Pulsante avvio
        self.start_button = tk.Button(
            main_frame,
            text="🚀 Installa Sistema",
            font=("Arial", 14, "bold"),
            bg='#3b82f6',
            fg='white',
            pady=10,
            command=self.start_setup
        )
        self.start_button.pack(pady=20)
        
        # Log area
        tk.Label(
            main_frame,
            text="📋 Log:",
            font=("Arial", 11, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w')
        
        log_frame = tk.Frame(main_frame)
        log_frame.pack(fill='both', expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, height=8, width=70, font=("Courier", 9))
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def choose_directory(self):
        """Scegli directory installazione"""
        directory = filedialog.askdirectory(title="Scegli directory installazione", initialdir=self.dir_var.get())
        if directory:
            self.dir_var.set(directory)
            self.install_dir = Path(directory) / "RAG_Psicologia_Sistema"
    
    def choose_database(self):
        """Scegli database - FIX: Imposta source_db_path"""
        directory = filedialog.askdirectory(title="Scegli cartella Rag_db", initialdir=self.db_var.get())
        if directory:
            db_path = Path(directory)
            if self.validate_database(db_path):
                self.db_var.set(str(db_path))
                self.source_db_path = db_path  # FIX: Imposta il percorso sorgente
                self.log("✅ Database selezionato: " + str(db_path))
            else:
                messagebox.showerror("Database Non Valido", "La cartella non contiene un database RAG valido.")
    
    def auto_detect_database(self):
        """Auto-rileva database - FIX: Imposta source_db_path"""
        search_paths = [
            Path.cwd() / "Rag_db",
            Path.cwd().parent / "Rag_db",
            Path(self.dir_var.get()) / "Rag_db",
        ]
        
        for db_path in search_paths:
            if self.validate_database(db_path):
                self.db_var.set(str(db_path))
                self.source_db_path = db_path  # FIX: Imposta il percorso sorgente
                self.log(f"✅ Database trovato: {db_path}")
                messagebox.showinfo("Database Trovato", f"Database rilevato: {db_path}")
                return
        
        messagebox.showwarning("Database Non Trovato", "Usa il pulsante 📂 per selezionare manualmente.")
    
    def test_database(self):
        """Test database selezionato"""
        db_path = Path(self.db_var.get())
        if self.validate_database(db_path):
            files_count = len(list(db_path.rglob('*')))
            messagebox.showinfo("Database Valido", f"✅ Database valido!\nFile trovati: {files_count}")
            self.source_db_path = db_path  # FIX: Imposta il percorso anche qui
        else:
            messagebox.showerror("Database Non Valido", "❌ La cartella non contiene un database RAG valido.")
    
    def validate_database(self, db_path):
        """Valida database"""
        if not db_path.exists() or not db_path.is_dir():
            return False
        
        files = list(db_path.iterdir())
        if not files:
            return False
        
        # Cerca file tipici ChromaDB
        has_db_files = any(f.name.endswith('.sqlite3') for f in files if f.is_file())
        has_uuid_dirs = any(len(f.name) == 36 and f.name.count('-') == 4 for f in files if f.is_dir())
        
        return has_db_files or has_uuid_dirs
    
    def log(self, message):
        """Log semplice"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_setup(self):
        """Avvia setup con validazioni migliorate"""
        self.api_key = self.api_entry.get().strip()
        if not self.api_key or not self.api_key.startswith('sk-'):
            messagebox.showerror("Errore", "Inserisci API Key OpenAI valida (inizia con 'sk-')")
            return
        
        # FIX: Verifica che source_db_path sia impostato
        if self.source_db_path is None:
            # Prova a impostarlo dal campo UI
            db_path = Path(self.db_var.get())
            if self.validate_database(db_path):
                self.source_db_path = db_path
                self.log(f"✅ Database impostato: {db_path}")
            else:
                messagebox.showerror("Errore", "Database non valido. Usa auto-rileva o seleziona manualmente.")
                return
        
        self.install_dir = Path(self.dir_var.get()) / "RAG_Psicologia_Sistema"
        self.start_button.config(state='disabled', text="⏳ Installazione...")
        
        # Avvia in thread
        setup_thread = threading.Thread(target=self.run_setup)
        setup_thread.daemon = True
        setup_thread.start()
    
    def run_setup(self):
        """Setup completo SEMPLICE"""
        try:
            self.log("🚀 Avviando installazione...")
            
            # 1. Prepara directory
            self.log("📁 Preparando directory...")
            if self.install_dir.exists():
                shutil.rmtree(self.install_dir)
            self.install_dir.mkdir(parents=True)
            
            # 2. Scarica Python
            self.log("📥 Scaricando Python embedded...")
            python_zip = self.install_dir / "python.zip"
            urllib.request.urlretrieve(self.python_embedded_url, python_zip)
            
            # 3. Estrai Python
            self.log("📦 Estraendo Python...")
            python_dir = self.install_dir / "python"
            with zipfile.ZipFile(python_zip, 'r') as zip_ref:
                zip_ref.extractall(python_dir)
            python_zip.unlink()
            
            # 4. Configura Python
            self.log("⚙️ Configurando Python...")
            self.configure_python_simple(python_dir)
            
            # 5. Installa pip
            self.log("🔧 Installando pip...")
            self.install_pip_simple(python_dir)
            
            # 6. Installa pacchetti
            self.log("📦 Installando pacchetti...")
            self.install_packages_simple(python_dir)
            
            # 7. Copia sistema
            self.log("📋 Copiando file sistema...")
            self.copy_system_files()
            
            # 8. Crea launcher
            self.log("🚀 Creando launcher...")
            self.create_launcher()
            
            self.log("✅ INSTALLAZIONE COMPLETATA!")
            self.setup_finished()
            
        except Exception as e:
            self.log(f"❌ ERRORE: {e}")
            self.setup_failed()
    
    def configure_python_simple(self, python_dir):
        """Configura Python embedded - SEMPLICE"""
        # Trova e modifica .pth file
        pth_files = list(python_dir.glob("python*._pth"))
        if pth_files:
            pth_file = pth_files[0]
            content = pth_file.read_text()
            if "#import site" in content:
                content = content.replace("#import site", "import site")
                pth_file.write_text(content)
    
    def install_pip_simple(self, python_dir):
        """Installa pip - SEMPLICE"""
        python_exe = python_dir / "python.exe"
        get_pip_path = python_dir / "get-pip.py"
        
        # Scarica get-pip.py
        urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip_path)
        
        # Installa pip - USA PERCORSO ESPLICITO
        subprocess.run([str(python_exe), str(get_pip_path)], cwd=str(python_dir), check=True)
    
    def install_packages_simple(self, python_dir):
        """Installa pacchetti - SEMPLICE"""
        python_exe = python_dir / "python.exe"
        
        packages = ["openai", "chromadb", "streamlit", "PyMuPDF", "Pillow", "nltk"]
        
        for package in packages:
            self.log(f"  📦 {package}...")
            # USA PERCORSO ESPLICITO - FIX Windows aliases
            subprocess.run([
                str(python_exe), "-m", "pip", "install", package, "--no-warn-script-location"
            ], cwd=str(python_dir), check=True)
    
    def copy_system_files(self):
        """Copia file sistema - FIX: Gestione corretta source_db_path"""
        # FIX: Verifica che source_db_path sia impostato
        if self.source_db_path is None:
            # Fallback: usa il percorso dal campo UI
            self.source_db_path = Path(self.db_var.get())
            
        if not self.source_db_path.exists():
            raise Exception(f"Database sorgente non trovato: {self.source_db_path}")
        
        # Copia database
        db_dest = self.install_dir / "Rag_db"
        self.log(f"📂 Copiando database: {self.source_db_path} → {db_dest}")
        shutil.copytree(self.source_db_path, db_dest)
        
        # Salva API key
        (self.install_dir / ".api_key").write_text(self.api_key)
        
        # Crea file Python
        (self.install_dir / "rag_system.py").write_text(self.get_rag_system_code())
        (self.install_dir / "web_app.py").write_text(self.get_web_app_code())
        (self.install_dir / "launcher.py").write_text(self.get_launcher_code())
    
    def create_launcher(self):
        """Crea launcher Windows - FIX: Escape corretto"""
        # FIX: Usa raw string per evitare problemi di escape
        launcher_content = f'''@echo off
cd /d "{self.install_dir}"
echo 🧠 Avviando Sistema RAG...
python\\python.exe launcher.py
if errorlevel 1 pause
'''
        (self.install_dir / "🚀 AVVIA_RAG_PSICOLOGIA.bat").write_text(launcher_content, encoding='utf-8')
    
    def setup_finished(self):
        """Setup completato"""
        self.start_button.config(state='normal', text="✅ Completato", bg='#10b981')
        messagebox.showinfo("Completato!", f"Sistema installato in:\n{self.install_dir}")
    
    def setup_failed(self):
        """Setup fallito"""
        self.start_button.config(state='normal', text="❌ Riprova", bg='#dc2626')
    
    def get_rag_system_code(self):
        """Codice rag_system.py"""
        return '''import os
import chromadb
from pathlib import Path
from typing import Dict
from openai import OpenAI

class SimpleRAGQuery:
    def __init__(self, openai_api_key: str, db_path: str = "./Rag_db"):
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.client = chromadb.PersistentClient(path=db_path)
    
    def search_and_respond(self, query: str, n_results: int = 5) -> Dict:
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small", input=[query]
            )
            query_embedding = response.data[0].embedding
            
            all_results = []
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                results = collection.query(
                    query_embeddings=[query_embedding], n_results=min(n_results, collection.count())
                )
                
                for i in range(len(results['documents'][0])):
                    all_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity': 1 - results['distances'][0][i],
                    })
            
            all_results.sort(key=lambda x: x['similarity'], reverse=True)
            top_results = all_results[:n_results]
            
            if not top_results:
                return {'query': query, 'response': "Nessuna informazione trovata.", 'sources': []}
            
            context = "\\n\\n".join([
                f"[FONTE] {Path(r['metadata']['source_file']).name}, pagina {r['metadata']['page_number']}:\\n{r['content']}"
                for r in top_results
            ])
            
            gpt_response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Rispondi basandoti sui documenti forniti. Cita sempre le fonti."},
                    {"role": "user", "content": f"DOMANDA: {query}\\n\\nDOCUMENTI:\\n{context}"}
                ],
                max_tokens=1500, temperature=0.2
            )
            
            return {
                'query': query,
                'response': gpt_response.choices[0].message.content,
                'sources': [{'file_name': Path(r['metadata']['source_file']).name, 
                           'page_number': r['metadata']['page_number'],
                           'similarity': r['similarity']} for r in top_results]
            }
            
        except Exception as e:
            return {'query': query, 'response': f"Errore: {str(e)}", 'sources': []}
'''
    
    def get_web_app_code(self):
        """Codice web_app.py"""
        return '''import streamlit as st
import os
from rag_system import SimpleRAGQuery

st.set_page_config(page_title="🧠 RAG Psicologia", page_icon="🧠", layout="wide")

st.markdown('<h1 style="text-align: center;">🧠 Sistema RAG - Consultazione Psicologia</h1>', unsafe_allow_html=True)

@st.cache_resource
def init_rag_system():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        try:
            with open('.api_key', 'r') as f:
                api_key = f.read().strip()
        except:
            return None
    
    try:
        return SimpleRAGQuery(api_key, db_path="./Rag_db")
    except Exception as e:
        st.error(f"Errore: {e}")
        return None

rag_system = init_rag_system()

if rag_system is None:
    st.error("❌ Sistema non configurato.")
    st.stop()

st.success("✅ Sistema RAG pronto!")

query = st.text_area("Inserisci la tua domanda:", placeholder="Es: Qual è la differenza tra ansia e angoscia?", height=100)

col1, col2 = st.columns(2)
with col1:
    n_sources = st.slider("Numero fonti", 3, 8, 5)
with col2:
    if st.button("🔍 Cerca Risposta", type="primary"):
        if query.strip():
            with st.spinner("🧠 Analizzando..."):
                result = rag_system.search_and_respond(query, n_sources)
            
            st.markdown("### 📝 Risposta")
            st.markdown(result['response'])
            
            if result['sources']:
                st.markdown("### 📚 Fonti")
                for i, source in enumerate(result['sources'], 1):
                    with st.expander(f"📄 {i}. {source['file_name']} (p.{source['page_number']})"):
                        st.write(f"Rilevanza: {source['similarity']:.3f}")
        else:
            st.error("Inserisci una domanda!")
'''
    
    def get_launcher_code(self):
        """Codice launcher.py - FIX: Escape corretto"""
        # FIX: Usa triple quotes e gestisci escape correttamente
        return """import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    # Imposta API key
    api_key_file = Path('.api_key')
    if api_key_file.exists():
        os.environ['OPENAI_API_KEY'] = api_key_file.read_text().strip()
    
    if not Path('Rag_db').exists():
        print("❌ Database non trovato!")
        input("Premi Invio...")
        return 1
    
    print("✅ Avviando sistema...")
    
    try:
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "web_app.py",
            "--server.address", "localhost", "--server.port", "8501",
            "--browser.gatherUsageStats", "false", "--server.headless", "true"
        ])
        
        time.sleep(3)
        webbrowser.open('http://localhost:8501')
        print("🌐 Sistema avviato: http://localhost:8501")
        
        input("Premi Invio per chiudere...")
        return 0
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        input("Premi Invio...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
"""

if __name__ == "__main__":
    app = SimpleRAGInstaller()
    app.root.mainloop()