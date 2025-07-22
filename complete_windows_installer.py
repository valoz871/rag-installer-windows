#!/usr/bin/env python3
"""
RAG Psicologia - COMPLETE WINDOWS INSTALLER
Creates a fully automated installer that:
1. Downloads and installs Python automatically
2. Installs all required packages
3. Sets up the complete RAG system
4. Creates desktop shortcuts
5. Works for non-technical users

To compile to EXE: pyinstaller --onefile --windowed complete_windows_installer.py
"""

import os
import sys
import subprocess
import urllib.request
import tempfile
import shutil
import time
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
import zipfile

class CompleteRAGInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema RAG Psicologia - Installer")  # Titolo più corto
        self.root.geometry("750x550")  # MOLTO PIU' PICCOLO per 800x600
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(False, False)
        
        # Configuration
        self.python_version = "3.11.9"
        self.python_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-amd64.exe"
        self.install_dir = Path.home() / "RAG_Psicologia"
        self.api_key = ""
        self.database_path = None
        self.cancel_requested = False
        
        self.create_interface()
    
    def create_interface(self):
        """Create installer GUI"""
        
        # Header MINI per risparmiare spazio
        header_frame = tk.Frame(self.root, bg='#1e3a8a', height=50)  # Molto ridotto
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="RAG Psicologia Installer",  # Titolo più corto
            font=("Arial", 14, "bold"),  # Molto ridotto
            fg="white",
            bg='#1e3a8a'
        )
        title_label.pack(pady=5)
        
        # NIENTE subtitle per risparmiare spazio
        
        # SCROLLABLE MAIN CONTENT - FIX PER RISOLUZIONI PICCOLE
        canvas = tk.Canvas(self.root, bg='#f0f8ff')
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f8ff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        # Main content (ora dentro scrollable_frame invece di main_frame)
        main_frame = tk.Frame(scrollable_frame, bg='#f0f8ff', padx=10, pady=15)  # Ridotto padding
        main_frame.pack(fill='both', expand=True)
        
        # Welcome message (molto più compatto)
        welcome_text = tk.Label(
            main_frame,
            text="Installer automatico: Python + librerie + sistema RAG + collegamenti desktop\nRichiede 5-10 minuti e connessione internet.",
            font=("Arial", 9),  # Più piccolo
            bg='#f0f8ff',
            fg='#374151',
            justify='left',
            wraplength=700
        )
        welcome_text.pack(pady=5)  # Molto ridotto
        
        # Configuration section (più compatta)
        config_frame = tk.LabelFrame(
            main_frame,
            text="⚙️ Configurazione",
            font=("Arial", 10, "bold"),
            bg='#f0f8ff',
            padx=8, pady=6  # Molto ridotto
        )
        config_frame.pack(fill='x', pady=5)
        
        # Install directory (compatto)
        tk.Label(
            config_frame,
            text="📁 Directory:",
            font=("Arial", 8, "bold"),  # Più piccolo
            bg='#f0f8ff'
        ).pack(anchor='w')
        
        dir_frame = tk.Frame(config_frame, bg='#f0f8ff')
        dir_frame.pack(fill='x', pady=2)
        
        self.dir_var = tk.StringVar(value=str(self.install_dir))
        dir_entry = tk.Entry(dir_frame, textvariable=self.dir_var, font=("Arial", 8))
        dir_entry.pack(side='left', fill='x', expand=True)
        
        tk.Button(dir_frame, text="📂", command=self.choose_directory, width=2, font=("Arial", 8)).pack(side='right', padx=(3, 0))
        
        # Database path (compatto)
        tk.Label(
            config_frame,
            text="🗄️ Database Rag_db:",
            font=("Arial", 8, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w', pady=(6, 0))
        
        db_frame = tk.Frame(config_frame, bg='#f0f8ff')
        db_frame.pack(fill='x', pady=2)
        
        self.db_var = tk.StringVar(value="Seleziona cartella Rag_db...")
        db_entry = tk.Entry(db_frame, textvariable=self.db_var, font=("Arial", 8))
        db_entry.pack(side='left', fill='x', expand=True)
        
        tk.Button(db_frame, text="📂", command=self.choose_database, width=2, font=("Arial", 8)).pack(side='right', padx=(3, 0))
        
        # Auto-detect button (più piccolo)
        tk.Button(
            config_frame,
            text="🔍 Auto-Rileva",
            command=self.auto_detect_database,
            bg='#6366f1',
            fg='white',
            font=("Arial", 8),
            pady=2  # Molto ridotto
        ).pack(pady=2)
        
        # API Key (compatto)
        tk.Label(
            config_frame,
            text="🔑 API Key OpenAI:",
            font=("Arial", 8, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w', pady=(6, 0))
        
        self.api_entry = tk.Entry(
            config_frame,
            font=("Arial", 8),  # Font ridotto
            show="*",
            width=60
        )
        self.api_entry.pack(fill='x', pady=2)
        
        tk.Label(
            config_frame,
            text="(Inizia con 'sk-')",
            font=("Arial", 7),  # Molto piccolo
            fg="gray",
            bg='#f0f8ff'
        ).pack(anchor='w')
        
        # Install button (più compatto ma visibile)
        button_frame = tk.Frame(main_frame, bg='#f0f8ff')
        button_frame.pack(fill='x', pady=8)  # Ridotto
        
        self.install_button = tk.Button(
            button_frame,
            text="🚀 Installa Sistema Completo",
            font=("Arial", 11, "bold"),  # Ridotto da 14 a 11
            bg='#059669',
            fg='white',
            pady=6,  # Molto ridotto
            command=self.start_installation
        )
        self.install_button.pack(side='left', fill='x', expand=True)
        
        self.cancel_button = tk.Button(
            button_frame,
            text="❌ Annulla",
            font=("Arial", 9),  # Ridotto
            bg='#dc2626',
            fg='white',
            pady=6,
            command=self.cancel_installation,
            state='disabled'
        )
        self.cancel_button.pack(side='right', padx=(8, 0))
        
        # Progress section (più compatto)
        progress_frame = tk.LabelFrame(
            main_frame,
            text="📊 Progresso",
            font=("Arial", 9, "bold"),
            bg='#f0f8ff'
        )
        progress_frame.pack(fill='x', pady=6)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=700
        )
        self.progress_bar.pack(pady=4, padx=10)  # Ridotto
        
        self.status_label = tk.Label(
            progress_frame,
            text="Pronto per l'installazione...",
            font=("Arial", 8),  # Font ridotto
            bg='#f0f8ff',
            fg='#374151'
        )
        self.status_label.pack(pady=(0, 4))
        
        # Log area - MOLTO PIU' GRANDE E VISIBILE
        log_frame = tk.LabelFrame(
            main_frame,
            text="📋 Log Dettagliato",
            font=("Arial", 9, "bold"),
            bg='#f0f8ff'
        )
        log_frame.pack(fill='both', expand=True, pady=5)
        
        log_container = tk.Frame(log_frame)
        log_container.pack(fill='both', expand=True, padx=6, pady=6)
        
        self.log_text = tk.Text(
            log_container,
            height=12,  # AUMENTATO da 6 a 12 righe
            font=("Courier", 7),  # Font più piccolo per vedere più testo
            bg='#ffffff',
            fg='#000000',
            wrap='word'
        )
        
        log_scrollbar = tk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def choose_directory(self):
        """Choose installation directory"""
        directory = filedialog.askdirectory(
            title="Scegli directory installazione",
            initialdir=str(self.install_dir.parent)
        )
        if directory:
            self.install_dir = Path(directory) / "RAG_Psicologia"
            self.dir_var.set(str(self.install_dir))
    
    def choose_database(self):
        """Choose database directory"""
        directory = filedialog.askdirectory(title="Seleziona cartella Rag_db")
        if directory:
            db_path = Path(directory)
            if self.validate_database(db_path):
                self.database_path = db_path
                self.db_var.set(str(db_path))
                self.log_message("Database selezionato e validato")
            else:
                messagebox.showerror("Database Non Valido", "La cartella selezionata non contiene un database RAG valido.")
    
    def auto_detect_database(self):
        """Auto-detect database in common locations"""
        search_paths = [
            Path.cwd() / "Rag_db",
            Path.cwd().parent / "Rag_db",  
            Path.home() / "Desktop" / "Rag_db",
            Path.home() / "Downloads" / "Rag_db"
        ]
        
        for db_path in search_paths:
            if self.validate_database(db_path):
                self.database_path = db_path
                self.db_var.set(str(db_path))
                self.log_message(f"Database auto-rilevato: {db_path}")
                messagebox.showinfo("Database Trovato", f"Database rilevato automaticamente:\n{db_path}")
                return
        
        messagebox.showwarning("Database Non Trovato", "Usa il pulsante 'Sfoglia' per selezionare manualmente la cartella Rag_db")
    
    def validate_database(self, db_path):
        """Validate RAG database"""
        if not db_path.exists() or not db_path.is_dir():
            return False
        
        # Check for ChromaDB files
        has_sqlite = any(f.name.endswith('.sqlite3') for f in db_path.rglob('*') if f.is_file())
        has_collections = any(len(d.name) == 36 and d.name.count('-') == 4 for d in db_path.iterdir() if d.is_dir())
        
        return has_sqlite or has_collections
    
    def log_message(self, message):
        """Add message to log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.log_text.insert(tk.END, f"{formatted_message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_progress(self, value, status):
        """Update progress bar and status"""
        self.progress_bar['value'] = value
        self.status_label.config(text=status)
        self.root.update()
    
    def start_installation(self):
        """Start complete installation"""
        # Validation
        self.api_key = self.api_entry.get().strip()
        if not self.api_key or not self.api_key.startswith('sk-'):
            messagebox.showerror("Errore", "Inserisci una API Key OpenAI valida (deve iniziare con 'sk-')")
            return
        
        if not self.database_path or not self.validate_database(self.database_path):
            messagebox.showerror("Errore", "Seleziona un database RAG valido")
            return
        
        self.install_dir = Path(self.dir_var.get())
        
        # Confirmation
        if not messagebox.askyesno(
            "Conferma Installazione",
            f"Installare il Sistema RAG in:\n{self.install_dir}\n\n"
            f"Database: {self.database_path}\n\n"
            "L'installazione richiede 5-10 minuti.\nContinuare?"
        ):
            return
        
        # Prepare UI
        self.install_button.config(state='disabled')
        self.cancel_button.config(state='normal')
        self.cancel_requested = False
        
        # Start installation in separate thread
        install_thread = threading.Thread(target=self.run_complete_installation)
        install_thread.daemon = True
        install_thread.start()
    
    def cancel_installation(self):
        """Cancel installation"""
        self.cancel_requested = True
        self.log_message("Installazione annullata dall'utente")
        self.install_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        self.update_progress(0, "Installazione annullata")
    
    def run_complete_installation(self):
        """Run complete installation process"""
        try:
            steps = [
                ("Preparazione", self.prepare_installation),
                ("Controllo Python", self.check_and_install_python),
                ("Installazione librerie", self.install_python_packages),
                ("Copia database", self.copy_database),
                ("Creazione sistema", self.create_system_files),
                ("Configurazione", self.setup_configuration),
                ("Creazione collegamenti", self.create_shortcuts),
                ("Test finale", self.test_installation)
            ]
            
            total_steps = len(steps)
            
            for i, (step_name, step_func) in enumerate(steps):
                if self.cancel_requested:
                    return
                
                progress = (i / total_steps) * 90  # Reserve 10% for completion
                self.update_progress(progress, f"{step_name}...")
                self.log_message(f"=== {step_name.upper()} ===")
                
                step_func()
                
                self.log_message(f"{step_name} completato con successo")
            
            # Installation completed
            self.update_progress(100, "Installazione completata!")
            self.log_message("=== INSTALLAZIONE COMPLETATA ===")
            
            self.installation_completed()
            
        except Exception as e:
            self.log_message(f"ERRORE: {str(e)}")
            self.installation_failed(str(e))
    
    def prepare_installation(self):
        """Prepare installation"""
        if self.install_dir.exists():
            shutil.rmtree(self.install_dir)
        self.install_dir.mkdir(parents=True)
        self.log_message(f"Directory di installazione creata: {self.install_dir}")
    
    def check_and_install_python(self):
        """Check if Python is installed, install if needed - WITH DETAILED DEBUG"""
        python_installed = False
        
        self.log_message("=== CONTROLLO PYTHON ===")
        
        # Check if Python is already available
        try:
            self.log_message("Verificando se Python è già installato...")
            result = subprocess.run(["python", "--version"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and "Python 3" in result.stdout:
                self.log_message(f"TROVATO: {result.stdout.strip()}")
                python_installed = True
            else:
                self.log_message(f"Python comando fallito: return code {result.returncode}")
                if result.stdout:
                    self.log_message(f"STDOUT: {result.stdout}")
                if result.stderr:
                    self.log_message(f"STDERR: {result.stderr}")
        except FileNotFoundError:
            self.log_message("Comando 'python' non trovato nel PATH")
        except subprocess.TimeoutExpired:
            self.log_message("Timeout verificando Python esistente")
        except Exception as e:
            self.log_message(f"Errore check Python: {e}")
        
        # Try python3 command as well
        if not python_installed:
            try:
                self.log_message("Provando comando 'python3'...")
                result = subprocess.run(["python3", "--version"], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.log_message(f"TROVATO python3: {result.stdout.strip()}")
                    python_installed = True
            except:
                self.log_message("Comando 'python3' non disponibile")
        
        if not python_installed:
            self.log_message("Python non trovato - procedendo con installazione...")
            
            try:
                # Check internet connection first
                self.log_message("Testando connessione internet...")
                test_conn = urllib.request.urlopen("https://www.google.com", timeout=10)
                self.log_message(f"Connessione OK: status {test_conn.getcode()}")
                test_conn.close()
            except Exception as e:
                self.log_message(f"ERRORE connessione internet: {e}")
                raise Exception("Connessione internet necessaria per scaricare Python")
            
            # Check disk space
            try:
                import shutil
                total, used, free = shutil.disk_usage(str(self.install_dir.parent))
                free_gb = free / (1024**3)
                self.log_message(f"Spazio libero: {free_gb:.1f} GB")
                if free_gb < 1.0:
                    raise Exception(f"Spazio insufficiente: {free_gb:.1f} GB disponibili, richiesto almeno 1 GB")
            except Exception as e:
                self.log_message(f"Errore check spazio disco: {e}")
            
            # Download Python installer
            python_installer = self.install_dir / f"python-{self.python_version}-installer.exe"
            
            self.log_message(f"Scaricando Python {self.python_version}...")
            self.log_message(f"URL: {self.python_url}")
            self.log_message(f"Destinazione: {python_installer}")
            
            try:
                # Download with progress
                def download_progress(block_num, block_size, total_size):
                    if total_size > 0:
                        percent = (block_num * block_size / total_size) * 100
                        if percent <= 100:
                            self.log_message(f"Download: {percent:.1f}%")
                
                urllib.request.urlretrieve(self.python_url, python_installer, reporthook=download_progress)
                
                # Verify download
                size_mb = python_installer.stat().st_size / (1024 * 1024)
                self.log_message(f"Download completato: {size_mb:.1f} MB")
                
                if size_mb < 10:  # Python installer should be at least 10MB
                    raise Exception(f"Download corrotto: dimensione {size_mb:.1f} MB troppo piccola")
                    
            except Exception as e:
                self.log_message(f"ERRORE download Python: {e}")
                raise Exception(f"Impossibile scaricare Python: {e}")
            
            # Install Python
            self.log_message("Avviando installazione Python...")
            self.log_message("NOTA: Potrebbe richiedere privilegi amministratore")
            
            install_cmd = [
                str(python_installer),
                "/quiet",           # Silent install
                "InstallAllUsers=1", # For all users
                "PrependPath=1",    # Add to PATH
                "Include_test=0",   # Don't include tests
                "SimpleInstall=1"   # Simple installation
            ]
            
            self.log_message(f"Comando installazione: {' '.join(install_cmd)}")
            
            try:
                result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=600)  # 10 minutes max
                
                self.log_message(f"Installazione Python terminata con codice: {result.returncode}")
                
                if result.stdout:
                    self.log_message(f"STDOUT: {result.stdout}")
                if result.stderr:
                    self.log_message(f"STDERR: {result.stderr}")
                
                if result.returncode != 0:
                    self.log_message("ERRORE: Installazione Python fallita!")
                    self.log_message("Possibili cause:")
                    self.log_message("1. Privilegi amministratore insufficienti")
                    self.log_message("2. Antivirus che blocca installazione")
                    self.log_message("3. Python già installato in modo conflittuale")
                    self.log_message("4. Sistema operativo non supportato")
                    
                    raise Exception(f"Installazione Python fallita con codice {result.returncode}")
                
            except subprocess.TimeoutExpired:
                self.log_message("TIMEOUT: Installazione Python troppo lenta (>10 minuti)")
                raise Exception("Installazione Python timeout")
            except Exception as e:
                self.log_message(f"ERRORE esecuzione installer Python: {e}")
                raise Exception(f"Errore installazione Python: {e}")
            
            # Clean up installer
            try:
                python_installer.unlink()
                self.log_message("File installer rimosso")
            except:
                self.log_message("Impossibile rimuovere installer (non critico)")
            
            self.log_message("Attendendo completamento installazione Python...")
            time.sleep(10)  # Wait for installation to fully complete
            
            # Verify installation worked
            self.log_message("Verificando installazione Python...")
            max_retries = 5
            for attempt in range(max_retries):
                try:
                    result = subprocess.run(["python", "--version"], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0 and "Python 3" in result.stdout:
                        self.log_message(f"SUCCESSO: Python installato - {result.stdout.strip()}")
                        python_installed = True
                        break
                    else:
                        self.log_message(f"Tentativo {attempt+1}: Python non ancora disponibile")
                        time.sleep(3)
                except Exception as e:
                    self.log_message(f"Tentativo {attempt+1}: Errore verifica - {e}")
                    time.sleep(3)
            
            if not python_installed:
                self.log_message("ERRORE: Python installato ma non disponibile nel PATH")
                self.log_message("Possibili soluzioni:")
                self.log_message("1. Riavviare il computer")
                self.log_message("2. Installare Python manualmente da python.org")
                self.log_message("3. Aggiungere Python al PATH manualmente")
                raise Exception("Python installato ma non funzionante - riavviare sistema")
        
        self.log_message("=== CONTROLLO PYTHON COMPLETATO ===")
        return python_installed
    
    def install_python_packages(self):
        """Install required Python packages"""
        packages = [
            "openai>=1.3.0",
            "chromadb>=0.4.15",
            "streamlit>=1.28.0", 
            "PyMuPDF>=1.23.0",
            "Pillow>=10.0.0",
            "numpy>=1.24.0"
        ]
        
        for i, package in enumerate(packages):
            if self.cancel_requested:
                return
            
            package_name = package.split('>=')[0]
            self.log_message(f"Installando {package_name}...")
            
            try:
                subprocess.run([
                    "python", "-m", "pip", "install", package, "--no-warn-script-location"
                ], check=True, capture_output=True)
                
                self.update_progress(20 + (i / len(packages)) * 30, f"Installato {package_name}")
                
            except subprocess.CalledProcessError:
                # Try without version requirement
                self.log_message(f"Tentativo alternativo per {package_name}...")
                subprocess.run([
                    "python", "-m", "pip", "install", package_name, "--no-warn-script-location"
                ], check=True)
    
    def copy_database(self):
        """Copy RAG database"""
        dest_db = self.install_dir / "Rag_db"
        
        self.log_message(f"Copiando database da {self.database_path}")
        shutil.copytree(self.database_path, dest_db)
        
        # Verify copy
        copied_size = sum(f.stat().st_size for f in dest_db.rglob('*') if f.is_file()) / 1024 / 1024
        self.log_message(f"Database copiato: {copied_size:.1f} MB")
    
    def create_system_files(self):
        """Create system files"""
        # Create rag_system.py (from your original)
        rag_system_code = '''import os
import chromadb
from pathlib import Path
from typing import List, Dict
from openai import OpenAI

class SimpleRAGQuery:
    def __init__(self, openai_api_key: str, db_path: str = "./Rag_db"):
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
    
    def search_and_respond(self, query: str, n_results: int = 5) -> Dict:
        """Ricerca e genera risposta"""
        try:
            # Genera embedding query
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=[query]
            )
            query_embedding = response.data[0].embedding
            
            # Cerca in tutte le collezioni
            all_results = []
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=min(n_results, collection.count())
                )
                
                for i in range(len(results['documents'][0])):
                    result = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity': 1 - results['distances'][0][i],
                    }
                    all_results.append(result)
            
            # Ordina per similarità
            all_results.sort(key=lambda x: x['similarity'], reverse=True)
            top_results = all_results[:n_results]
            
            if not top_results:
                return {
                    'query': query,
                    'response': "Non ho trovato informazioni rilevanti.",
                    'sources': []
                }
            
            # Genera risposta con GPT
            context = "\\n\\n".join([
                f"[FONTE] {Path(r['metadata']['source_file']).name}, pagina {r['metadata']['page_number']}:\\n{r['content']}"
                for r in top_results
            ])
            
            gpt_response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sei un esperto di psicologia. Rispondi basandoti sui documenti forniti. Cita sempre le fonti nel formato [Fonte: nome_file.pdf, pagina X]."},
                    {"role": "user", "content": f"DOMANDA: {query}\\n\\nDOCUMENTI:\\n{context}"}
                ],
                max_tokens=1500,
                temperature=0.2
            )
            
            return {
                'query': query,
                'response': gpt_response.choices[0].message.content,
                'sources': [
                    {
                        'file_name': Path(r['metadata']['source_file']).name,
                        'page_number': r['metadata']['page_number'],
                        'similarity': r['similarity'],
                        'content_preview': r['content'][:200] + "..."
                    }
                    for r in top_results
                ]
            }
            
        except Exception as e:
            return {
                'query': query,
                'response': f"Errore: {str(e)}",
                'sources': []
            }
'''
        
        # Create web_app.py (from your original, simplified)
        web_app_code = '''import streamlit as st
import os
from rag_system import SimpleRAGQuery

st.set_page_config(
    page_title="RAG Psicologia",
    page_icon="brain",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTextArea textarea {
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">Sistema RAG - Consultazione Psicologia</h1>', unsafe_allow_html=True)

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
        st.error(f"Errore connessione: {e}")
        return None

rag_system = init_rag_system()

if rag_system is None:
    st.error("Sistema non configurato. Controlla API Key.")
    st.stop()

st.success("Sistema RAG connesso e pronto!")

st.subheader("Fai la Tua Domanda")

query = st.text_area(
    "Inserisci la tua domanda psicologica:",
    placeholder="Es: Qual è la differenza tra ansia e angoscia secondo questi autori?",
    height=100
)

col1, col2 = st.columns(2)
with col1:
    n_sources = st.slider("Numero fonti", 3, 8, 5)
with col2:
    if st.button("Cerca Risposta", type="primary"):
        if query.strip():
            with st.spinner("Analizzando documenti..."):
                result = rag_system.search_and_respond(query, n_sources)
            
            st.markdown("### Risposta")
            st.markdown(result['response'])
            
            if result['sources']:
                st.markdown("### Fonti Consultate")
                for i, source in enumerate(result['sources'], 1):
                    with st.expander(f"{i}. {source['file_name']} (p.{source['page_number']}) - Rilevanza: {source['similarity']:.3f}"):
                        st.text(source['content_preview'])
        else:
            st.error("Inserisci una domanda!")

with st.expander("Esempi di Domande"):
    st.markdown("""
    **Teoria e Concetti:**
    - "Qual è la differenza tra ansia e angoscia?"
    - "Come viene definito il transfert?"
    - "Cosa significa resistenza in terapia?"
    
    **Confronti Teorici:**
    - "Differenze tra Jung e Freud sull'inconscio?"
    - "Approccio cognitivo vs psicodinamico?"
    
    **Applicazioni Cliniche:**
    - "Caratteristiche del disturbo borderline?"
    - "Come si manifesta un episodio maniacale?"
    """)
'''
        
        # Create launcher
        launcher_code = '''import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    print("Sistema RAG Psicologia")
    print("=" * 40)
    
    # Set API key
    api_key_file = Path('.api_key')
    if api_key_file.exists():
        api_key = api_key_file.read_text().strip()
        os.environ['OPENAI_API_KEY'] = api_key
        print("API Key caricata")
    else:
        print("ERRORE: API Key non trovata")
        input("Premi Invio per uscire...")
        return 1
    
    # Check database
    if not Path('Rag_db').exists():
        print("ERRORE: Database non trovato")
        input("Premi Invio per uscire...")
        return 1
    
    print("Avviando sistema...")
    
    try:
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "web_app.py",
            "--server.address", "localhost", "--server.port", "8501",
            "--browser.gatherUsageStats", "false", "--server.headless", "true"
        ])
        
        time.sleep(3)
        webbrowser.open('http://localhost:8501')
        print("Sistema avviato: http://localhost:8501")
        
        input("Premi Invio per chiudere...")
        return 0
        
    except Exception as e:
        print(f"Errore: {e}")
        input("Premi Invio...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
        
        # Write files
        (self.install_dir / "rag_system.py").write_text(rag_system_code, encoding='utf-8')
        (self.install_dir / "web_app.py").write_text(web_app_code, encoding='utf-8')
        (self.install_dir / "launcher.py").write_text(launcher_code, encoding='utf-8')
        
        self.log_message("File di sistema creati")
    
    def setup_configuration(self):
        """Setup configuration"""
        # Save API key
        api_file = self.install_dir / ".api_key"
        api_file.write_text(self.api_key, encoding='utf-8')
        
        # Create batch launcher
        batch_content = f'''@echo off
cd /d "{self.install_dir}"
title Sistema RAG Psicologia

echo.
echo ================================
echo    Sistema RAG Psicologia
echo ================================
echo.

python launcher.py
'''
        
        batch_file = self.install_dir / "Avvia_RAG_Psicologia.bat"
        batch_file.write_text(batch_content, encoding='utf-8')
        
        self.log_message("Configurazione completata")
    
    def create_shortcuts(self):
        """Create desktop shortcuts"""
        try:
            desktop = Path.home() / "Desktop"
            shortcut_path = desktop / "Sistema RAG Psicologia.bat"
            
            shortcut_content = f'''@echo off
cd /d "{self.install_dir}"
python launcher.py
'''
            
            shortcut_path.write_text(shortcut_content, encoding='utf-8')
            self.log_message("Collegamento desktop creato")
            
        except Exception as e:
            self.log_message(f"Impossibile creare collegamento desktop: {e}")
    
    def test_installation(self):
        """Test installation"""
        # Test Python imports
        test_script = '''
try:
    import openai
    import chromadb
    import streamlit
    print("SUCCESS: All packages imported")
except ImportError as e:
    print(f"ERROR: {e}")
    exit(1)
'''
        
        test_file = self.install_dir / "test_install.py"
        test_file.write_text(test_script, encoding='utf-8')
        
        result = subprocess.run([
            "python", str(test_file)
        ], cwd=str(self.install_dir), capture_output=True, text=True)
        
        test_file.unlink()
        
        if result.returncode == 0:
            self.log_message("Test installazione: OK")
        else:
            raise Exception(f"Test fallito: {result.stderr}")
    
    def installation_completed(self):
        """Called when installation is completed"""
        self.install_button.config(
            state='normal',
            text="Installazione Completata!",
            bg='#10b981'
        )
        self.cancel_button.config(state='disabled')
        
        success_message = (
            f"Installazione completata con successo!\n\n"
            f"Il sistema è installato in:\n{self.install_dir}\n\n"
            f"Per avviare il sistema:\n"
            f"• Doppio-click su 'Sistema RAG Psicologia' sul desktop\n"
            f"• Oppure esegui 'Avvia_RAG_Psicologia.bat'\n\n"
            f"Il sistema si aprirà automaticamente nel browser."
        )
        
        messagebox.showinfo("Installazione Completata", success_message)
    
    def installation_failed(self, error):
        """Called when installation fails"""
        self.install_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        self.update_progress(0, "Installazione fallita")
        
        messagebox.showerror(
            "Errore Installazione",
            f"Installazione fallita:\n\n{error}\n\n"
            "Controlla il log per maggiori dettagli."
        )
    
    def run(self):
        """Run installer"""
        self.root.mainloop()

if __name__ == "__main__":
    installer = CompleteRAGInstaller()
    installer.run()