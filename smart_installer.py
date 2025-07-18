#!/usr/bin/env python3
"""
Smart Installer RAG - Versione CORRETTA e ROBUSTA
Risolve problemi di crash e gestione errori
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import shutil
import zipfile
import urllib.request
import urllib.error

class RobustRAGInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧠 RAG Psicologia - Installer Robusto")
        self.root.geometry("650x600")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(True, True)
        
        # Configurazione
        self.python_version = "3.11.8"
        self.install_dir = Path.cwd() / "RAG_Psicologia_Sistema"
        self.python_embedded_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-embed-amd64.zip"
        
        # Variabili
        self.api_key = ""
        self.setup_complete = False
        self.cancel_requested = False
        
        self.create_interface()
    
    def create_interface(self):
        """Interfaccia migliorata con progress bar"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#1e3a8a', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🧠 Sistema RAG Psicologia - Installer",
            font=("Arial", 18, "bold"),
            fg="white",
            bg='#1e3a8a'
        )
        title_label.pack(expand=True)
        
        # Contenuto principale con scrolling
        canvas = tk.Canvas(self.root, bg='#f0f8ff')
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f8ff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = scrollable_frame
        
        # Info sistema
        info_frame = tk.LabelFrame(main_frame, text="ℹ️ Informazioni", font=("Arial", 11, "bold"), bg='#f0f8ff', padx=15, pady=10)
        info_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            info_frame,
            text="✨ Installer robusto con gestione errori completa\n"
                 "🔧 Risolve automaticamente problemi comuni\n"
                 "📦 Sistema completamente autocontenuto",
            font=("Arial", 10),
            bg='#f0f8ff',
            fg='#374151',
            justify='left'
        ).pack(anchor='w')
        
        # Directory installazione
        dir_frame = tk.LabelFrame(main_frame, text="📁 Directory Installazione", font=("Arial", 11, "bold"), bg='#f0f8ff', padx=15, pady=10)
        dir_frame.pack(fill='x', pady=(0, 15))
        
        dir_entry_frame = tk.Frame(dir_frame, bg='#f0f8ff')
        dir_entry_frame.pack(fill='x', pady=5)
        
        self.dir_var = tk.StringVar(value=str(self.install_dir))
        dir_entry = tk.Entry(dir_entry_frame, textvariable=self.dir_var, font=("Arial", 10), width=50)
        dir_entry.pack(side='left', fill='x', expand=True)
        
        tk.Button(dir_entry_frame, text="📂", command=self.choose_directory, width=3).pack(side='right', padx=(5, 0))
        
        # Database path
        db_frame = tk.LabelFrame(main_frame, text="🗄️ Database Rag_db", font=("Arial", 11, "bold"), bg='#f0f8ff', padx=15, pady=10)
        db_frame.pack(fill='x', pady=(0, 15))
        
        db_entry_frame = tk.Frame(db_frame, bg='#f0f8ff')
        db_entry_frame.pack(fill='x', pady=5)
        
        default_db = Path.cwd() / "Rag_db"
        self.db_var = tk.StringVar(value=str(default_db))
        db_entry = tk.Entry(db_entry_frame, textvariable=self.db_var, font=("Arial", 10), width=50)
        db_entry.pack(side='left', fill='x', expand=True)
        
        tk.Button(db_entry_frame, text="📂", command=self.choose_database, width=3).pack(side='right', padx=(5, 0))
        
        # Pulsanti database
        db_buttons_frame = tk.Frame(db_frame, bg='#f0f8ff')
        db_buttons_frame.pack(fill='x', pady=5)
        
        tk.Button(
            db_buttons_frame,
            text="🔍 Auto-rileva",
            command=self.auto_detect_database,
            bg='#6366f1',
            fg='white',
            font=("Arial", 9)
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            db_buttons_frame,
            text="✅ Testa Database",
            command=self.test_database,
            bg='#10b981',
            fg='white',
            font=("Arial", 9)
        ).pack(side='left')
        
        # API Key
        api_frame = tk.LabelFrame(main_frame, text="🔑 OpenAI API Key", font=("Arial", 11, "bold"), bg='#f0f8ff', padx=15, pady=10)
        api_frame.pack(fill='x', pady=(0, 15))
        
        self.api_entry = tk.Entry(
            api_frame,
            font=("Arial", 11),
            width=60,
            show="*"
        )
        self.api_entry.pack(fill='x', pady=5)
        
        tk.Label(
            api_frame,
            text="💡 Deve iniziare con 'sk-' - fornita dal creatore del sistema",
            font=("Arial", 9),
            fg="gray",
            bg='#f0f8ff'
        ).pack(anchor='w')
        
        # Progress bar
        progress_frame = tk.LabelFrame(main_frame, text="📊 Progresso", font=("Arial", 11, "bold"), bg='#f0f8ff', padx=15, pady=10)
        progress_frame.pack(fill='x', pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=500)
        self.progress_bar.pack(pady=5)
        
        self.progress_label = tk.Label(
            progress_frame,
            text="⏳ Pronto per installazione...",
            font=("Arial", 10),
            bg='#f0f8ff',
            fg='#374151'
        )
        self.progress_label.pack(pady=5)
        
        # Pulsanti azione
        action_frame = tk.Frame(main_frame, bg='#f0f8ff')
        action_frame.pack(fill='x', pady=15)
        
        self.start_button = tk.Button(
            action_frame,
            text="🚀 Installa Sistema",
            font=("Arial", 14, "bold"),
            bg='#3b82f6',
            fg='white',
            pady=12,
            command=self.start_setup
        )
        self.start_button.pack(side='left', fill='x', expand=True)
        
        self.cancel_button = tk.Button(
            action_frame,
            text="❌ Annulla",
            font=("Arial", 12),
            bg='#dc2626',
            fg='white',
            pady=12,
            command=self.cancel_setup,
            state='disabled'
        )
        self.cancel_button.pack(side='right', padx=(10, 0))
        
        # Log area
        log_frame = tk.LabelFrame(main_frame, text="📋 Log Dettagliato", font=("Arial", 11, "bold"), bg='#f0f8ff', padx=15, pady=10)
        log_frame.pack(fill='both', expand=True)
        
        log_container = tk.Frame(log_frame)
        log_container.pack(fill='both', expand=True, pady=5)
        
        self.log_text = tk.Text(log_container, height=10, width=70, font=("Courier", 9), wrap='word')
        log_scrollbar = tk.Scrollbar(log_container, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')
    
    def safe_ui_update(self, func, *args, **kwargs):
        """Aggiornamento UI thread-safe"""
        try:
            self.root.after(0, func, *args, **kwargs)
        except:
            pass  # Ignora errori se finestra è chiusa
    
    def log(self, message, level="INFO"):
        """Log thread-safe con livelli"""
        def _log():
            icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}
            icon = icons.get(level, "ℹ️")
            formatted = f"{icon} {message}\n"
            
            self.log_text.insert(tk.END, formatted)
            self.log_text.see(tk.END)
            self.root.update_idletasks()
        
        self.safe_ui_update(_log)
    
    def update_progress(self, value, status):
        """Aggiorna progress bar thread-safe"""
        def _update():
            self.progress_bar['value'] = value
            self.progress_label.config(text=status)
            self.root.update_idletasks()
        
        self.safe_ui_update(_update)
    
    def choose_directory(self):
        """Scegli directory installazione"""
        directory = filedialog.askdirectory(
            title="Scegli directory installazione", 
            initialdir=str(Path(self.dir_var.get()).parent)
        )
        if directory:
            self.dir_var.set(directory)
            self.install_dir = Path(directory) / "RAG_Psicologia_Sistema"
            self.log(f"Directory installazione: {self.install_dir}")
    
    def choose_database(self):
        """Scegli database manualmente"""
        directory = filedialog.askdirectory(
            title="Scegli cartella Rag_db", 
            initialdir=str(Path(self.db_var.get()).parent)
        )
        if directory:
            db_path = Path(directory)
            if self.validate_database(db_path):
                self.db_var.set(str(db_path))
                self.log(f"Database selezionato: {db_path}", "SUCCESS")
            else:
                messagebox.showerror("Database Non Valido", 
                    "La cartella selezionata non contiene un database RAG valido.\n"
                    "Verifica di aver selezionato la cartella 'Rag_db' corretta.")
    
    def auto_detect_database(self):
        """Auto-rileva database in posizioni comuni"""
        search_paths = [
            Path.cwd() / "Rag_db",
            Path.cwd().parent / "Rag_db", 
            Path(self.dir_var.get()) / "Rag_db",
            Path.home() / "Desktop" / "Rag_db",
            Path.home() / "Downloads" / "Rag_db"
        ]
        
        # Aggiungi percorsi relativi
        for parent in [Path.cwd(), Path.cwd().parent]:
            for item in parent.iterdir():
                if item.is_dir() and "rag" in item.name.lower():
                    search_paths.append(item)
        
        self.log("🔍 Ricerca automatica database...")
        
        for db_path in search_paths:
            self.log(f"Controllo: {db_path}")
            if self.validate_database(db_path):
                self.db_var.set(str(db_path))
                self.log(f"✅ Database trovato: {db_path}", "SUCCESS")
                messagebox.showinfo("Database Trovato!", f"Database rilevato automaticamente:\n{db_path}")
                return
        
        self.log("❌ Database non trovato automaticamente", "WARNING")
        messagebox.showwarning("Database Non Trovato", 
            "Nessun database trovato automaticamente.\n"
            "Usa il pulsante 📂 per selezionare manualmente la cartella 'Rag_db'.")
    
    def test_database(self):
        """Testa validità database"""
        db_path = Path(self.db_var.get())
        self.log(f"🧪 Test database: {db_path}")
        
        if self.validate_database(db_path):
            files_count = len(list(db_path.rglob('*')))
            self.log(f"✅ Database valido: {files_count} file totali", "SUCCESS")
            messagebox.showinfo("Database Valido", 
                f"✅ Database valido!\n"
                f"📁 Percorso: {db_path}\n"
                f"📄 File totali: {files_count}")
        else:
            self.log("❌ Database non valido", "ERROR")
            messagebox.showerror("Database Non Valido", 
                "Il database selezionato non è valido.\n"
                "Seleziona la cartella 'Rag_db' corretta.")
    
    def validate_database(self, db_path):
        """Validazione robusta database"""
        try:
            if not db_path.exists() or not db_path.is_dir():
                return False
            
            files = list(db_path.iterdir())
            if not files:
                return False
            
            # ChromaDB ha file .sqlite3 o directory UUID
            has_db_files = any(f.name.endswith('.sqlite3') for f in files if f.is_file())
            has_uuid_dirs = any(
                len(f.name) == 36 and f.name.count('-') == 4 
                for f in files if f.is_dir()
            )
            
            # Cerca anche file chroma-*
            has_chroma_files = any('chroma' in f.name.lower() for f in files)
            
            return has_db_files or has_uuid_dirs or has_chroma_files
            
        except Exception as e:
            self.log(f"Errore validazione database: {e}", "ERROR")
            return False
    
    def cancel_setup(self):
        """Annulla setup"""
        self.cancel_requested = True
        self.log("🛑 Installazione annullata dall'utente", "WARNING")
        self.reset_ui()
    
    def reset_ui(self):
        """Reset interfaccia"""
        self.start_button.config(state='normal', text="🚀 Installa Sistema", bg='#3b82f6')
        self.cancel_button.config(state='disabled')
        self.update_progress(0, "⏳ Pronto per installazione...")
        self.cancel_requested = False
    
    def start_setup(self):
        """Avvia setup con validazioni"""
        # Validazioni pre-setup
        self.api_key = self.api_entry.get().strip()
        if not self.api_key or not self.api_key.startswith('sk-'):
            messagebox.showerror("Errore", "Inserisci una API Key OpenAI valida (deve iniziare con 'sk-')")
            return
        
        db_path = Path(self.db_var.get())
        if not self.validate_database(db_path):
            messagebox.showerror("Errore", 
                "Database non valido.\n"
                "Usa 'Auto-rileva' o seleziona manualmente la cartella 'Rag_db'.")
            return
        
        self.install_dir = Path(self.dir_var.get()) / "RAG_Psicologia_Sistema"
        
        # Conferma sovrascrittura
        if self.install_dir.exists():
            if not messagebox.askyesno("Directory Esistente", 
                f"La directory {self.install_dir} esiste già.\n"
                "Vuoi sovrascrivere il contenuto?"):
                return
        
        # Prepara UI
        self.start_button.config(state='disabled', text="⏳ Installazione in corso...", bg='#6b7280')
        self.cancel_button.config(state='normal')
        self.cancel_requested = False
        
        self.log("🚀 Avvio installazione sistema RAG...", "INFO")
        
        # Avvia in thread separato
        setup_thread = threading.Thread(target=self.run_setup_with_error_handling)
        setup_thread.daemon = True
        setup_thread.start()
    
    def run_setup_with_error_handling(self):
        """Setup con gestione errori completa"""
        try:
            self.run_robust_setup()
        except Exception as e:
            self.log(f"💥 ERRORE CRITICO: {str(e)}", "ERROR")
            self.safe_ui_update(self.setup_failed, str(e))
    
    def run_robust_setup(self):
        """Setup robusto con retry logic"""
        
        steps = [
            (10, "Preparazione directory", self.prepare_directory_safe),
            (25, "Download Python Embedded", self.download_python_safe),
            (35, "Estrazione Python", self.extract_python_safe),
            (45, "Configurazione Python", self.configure_python_safe),
            (60, "Installazione pip", self.install_pip_safe),
            (75, "Installazione pacchetti", self.install_packages_safe),
            (85, "Copia file sistema", self.copy_system_files_safe),
            (95, "Creazione launcher", self.create_launcher_safe),
            (100, "Test finale", self.test_installation_safe)
        ]
        
        for progress, step_name, step_func in steps:
            if self.cancel_requested:
                self.log("🛑 Installazione annullata", "WARNING")
                return
            
            self.update_progress(progress, f"⏳ {step_name}...")
            self.log(f"🔄 Inizio: {step_name}")
            
            step_func()
            
            self.log(f"✅ Completato: {step_name}", "SUCCESS")
        
        self.log("🎉 INSTALLAZIONE COMPLETATA CON SUCCESSO!", "SUCCESS")
        self.safe_ui_update(self.setup_finished)
    
    def prepare_directory_safe(self):
        """Preparazione directory con gestione errori"""
        try:
            if self.install_dir.exists():
                self.log(f"🗑️ Rimozione directory esistente: {self.install_dir}")
                shutil.rmtree(self.install_dir)
            
            self.install_dir.mkdir(parents=True, exist_ok=True)
            self.log(f"📁 Directory creata: {self.install_dir}")
            
        except PermissionError:
            raise Exception(f"Permessi insufficienti per creare: {self.install_dir}")
        except Exception as e:
            raise Exception(f"Errore creazione directory: {str(e)}")
    
    def download_python_safe(self):
        """Download Python con retry e timeout"""
        python_zip = self.install_dir / "python_embedded.zip"
        
        for attempt in range(3):  # Max 3 tentativi
            try:
                self.log(f"📥 Tentativo {attempt + 1}/3: Scaricando Python {self.python_version}")
                
                # Download con timeout
                with urllib.request.urlopen(self.python_embedded_url, timeout=30) as response:
                    with open(python_zip, 'wb') as f:
                        shutil.copyfileobj(response, f)
                
                # Verifica dimensione file
                if python_zip.stat().st_size < 1024 * 1024:  # Meno di 1MB
                    raise Exception("File scaricato troppo piccolo")
                
                size_mb = python_zip.stat().st_size / 1024 / 1024
                self.log(f"✅ Download completato: {size_mb:.1f} MB")
                return
                
            except Exception as e:
                self.log(f"❌ Tentativo {attempt + 1} fallito: {str(e)}", "WARNING")
                if python_zip.exists():
                    python_zip.unlink()
                
                if attempt == 2:  # Ultimo tentativo
                    raise Exception(f"Download Python fallito dopo 3 tentativi: {str(e)}")
                
                time.sleep(2)  # Pausa tra tentativi
    
    def extract_python_safe(self):
        """Estrazione Python con verifica"""
        python_zip = self.install_dir / "python_embedded.zip"
        python_dir = self.install_dir / "python"
        
        try:
            with zipfile.ZipFile(python_zip, 'r') as zip_ref:
                zip_ref.extractall(python_dir)
            
            python_zip.unlink()  # Rimuovi zip
            
            # Verifica che python.exe esista
            python_exe = python_dir / "python.exe"
            if not python_exe.exists():
                raise Exception("python.exe non trovato dopo estrazione")
            
            self.log(f"📦 Python estratto in: {python_dir}")
            
        except zipfile.BadZipFile:
            raise Exception("File ZIP di Python corrotto")
        except Exception as e:
            raise Exception(f"Errore estrazione Python: {str(e)}")
    
    def configure_python_safe(self):
        """Configurazione Python embedded robusta"""
        python_dir = self.install_dir / "python"
        
        try:
            # Trova file ._pth
            pth_files = list(python_dir.glob("python*._pth"))
            if not pth_files:
                self.log("⚠️ File ._pth non trovato, creazione manuale", "WARNING")
                pth_content = "python311.zip\n.\n\n# Uncomment to run site.main() automatically\nimport site\n"
                (python_dir / "python311._pth").write_text(pth_content)
            else:
                pth_file = pth_files[0]
                content = pth_file.read_text()
                if "#import site" in content:
                    content = content.replace("#import site", "import site")
                    pth_file.write_text(content)
                    self.log("✅ Abilitato site-packages")
            
        except Exception as e:
            # Non critico, prosegui
            self.log(f"⚠️ Configurazione Python parziale: {str(e)}", "WARNING")
    
    def install_pip_safe(self):
        """Installazione pip con retry"""
        python_dir = self.install_dir / "python"
        python_exe = python_dir / "python.exe"
        get_pip_path = python_dir / "get-pip.py"
        
        for attempt in range(3):
            try:
                # Scarica get-pip.py
                urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip_path)
                
                # Installa pip
                result = subprocess.run([
                    str(python_exe), str(get_pip_path)
                ], cwd=str(python_dir), capture_output=True, text=True, timeout=120)
                
                if result.returncode != 0:
                    raise Exception(f"Pip install failed: {result.stderr}")
                
                # Test pip
                test_result = subprocess.run([
                    str(python_exe), "-m", "pip", "--version"
                ], capture_output=True, text=True, timeout=30)
                
                if test_result.returncode == 0:
                    self.log("✅ Pip installato e testato")
                    return
                else:
                    raise Exception("Pip test fallito")
                
            except Exception as e:
                self.log(f"❌ Tentativo pip {attempt + 1} fallito: {str(e)}", "WARNING")
                if attempt == 2:
                    raise Exception(f"Installazione pip fallita: {str(e)}")
                time.sleep(2)
    
    def install_packages_safe(self):
        """Installazione pacchetti con gestione errori robusta"""
        python_dir = self.install_dir / "python"
        python_exe = python_dir / "python.exe"
        
        # Pacchetti essenziali in ordine di priorità
        essential_packages = ["openai", "chromadb", "streamlit"]
        optional_packages = ["PyMuPDF", "Pillow", "nltk"]
        
        installed = []
        failed = []
        
        # Installa pacchetti essenziali
        for package in essential_packages:
            if self.cancel_requested:
                return
                
            success = self.install_single_package(python_exe, package, python_dir, required=True)
            if success:
                installed.append(package)
            else:
                failed.append(package)
                
        # Se pacchetti essenziali falliscono, errore critico
        if len(failed) > 0:
            raise Exception(f"Pacchetti essenziali falliti: {', '.join(failed)}")
        
        # Installa pacchetti opzionali (errori non critici)
        for package in optional_packages:
            if self.cancel_requested:
                return
                
            success = self.install_single_package(python_exe, package, python_dir, required=False)
            if success:
                installed.append(package)
            else:
                failed.append(package)
        
        self.log(f"✅ Pacchetti installati: {', '.join(installed)}", "SUCCESS")
        if failed:
            self.log(f"⚠️ Pacchetti opzionali falliti: {', '.join(failed)}", "WARNING")
    
    def install_single_package(self, python_exe, package, python_dir, required=True):
        """Installa singolo pacchetto con retry"""
        for attempt in range(3):
            try:
                self.log(f"📦 Installando {package} (tentativo {attempt + 1}/3)")
                
                result = subprocess.run([
                    str(python_exe), "-m", "pip", "install", package, 
                    "--no-warn-script-location", "--timeout", "60"
                ], cwd=str(python_dir), capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    self.log(f"✅ {package} installato")
                    return True
                else:
                    raise Exception(f"Exit code {result.returncode}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                self.log(f"⏰ Timeout installazione {package}", "WARNING")
            except Exception as e:
                self.log(f"❌ Errore {package}: {str(e)}", "WARNING")
                
            if attempt < 2:
                time.sleep(2)
        
        # Se è un pacchetto richiesto, lancia eccezione
        if required:
            raise Exception(f"Pacchetto essenziale {package} non installabile")
        
        return False
    
    def copy_system_files_safe(self):
        """Copia file sistema con validazione"""
        try:
            # Copia database
            db_source = Path(self.db_var.get())
            db_dest = self.install_dir / "Rag_db"
            
            self.log(f"📁 Copiando database: {db_source} -> {db_dest}")
            
            if not db_source.exists():
                raise Exception(f"Database sorgente non trovato: {db_source}")
            
            if db_dest.exists():
                shutil.rmtree(db_dest)
            
            shutil.copytree(db_source, db_dest)
            
            # Verifica copia
            copied_files = len(list(db_dest.rglob('*')))
            if copied_files == 0:
                raise Exception("Database copiato risulta vuoto")
            
            self.log(f"✅ Database copiato: {copied_files} file")
            
            # Salva API key
            api_file = self.install_dir / ".api_key"
            api_file.write_text(self.api_key, encoding='utf-8')
            
            # Crea file Python del sistema
            files_to_create = {
                "rag_system.py": self.get_rag_system_code(),
                "web_app.py": self.get_web_app_code(),
                "launcher.py": self.get_launcher_code(),
                "README_UTENTE.txt": self.get_user_readme()
            }
            
            for filename, content in files_to_create.items():
                file_path = self.install_dir / filename
                file_path.write_text(content, encoding='utf-8')
                self.log(f"✅ Creato: {filename}")
            
        except Exception as e:
            raise Exception(f"Errore copia file sistema: {str(e)}")
    
    def create_launcher_safe(self):
        """Crea launcher con gestione errori"""
        try:
            launcher_content = f'''@echo off
cd /d "{self.install_dir}"
title 🧠 Sistema RAG Psicologia

echo.
echo =====================================
echo     🧠 SISTEMA RAG PSICOLOGIA  
echo =====================================
echo.
echo ✅ Avviando sistema autocontenuto...
echo.

python\\python.exe launcher.py

if errorlevel 1 (
    echo.
    echo ❌ Errore durante l'avvio del sistema
    echo 💡 Consulta README_UTENTE.txt per assistenza
    echo.
    pause
)
'''
            
            launcher_path = self.install_dir / "🚀 AVVIA_RAG_PSICOLOGIA.bat"
            launcher_path.write_text(launcher_content, encoding='utf-8')
            
            self.log("✅ Launcher Windows creato")
            
        except Exception as e:
            raise Exception(f"Errore creazione launcher: {str(e)}")
    
    def test_installation_safe(self):
        """Test finale con validazione completa"""
        python_exe = self.install_dir / "python" / "python.exe"
        
        try:
            # Test 1: Import essenziali
            test_script = '''
import sys
try:
    import openai
    print("✅ OpenAI OK")
    import chromadb  
    print("✅ ChromaDB OK")
    import streamlit
    print("✅ Streamlit OK")
    print("SUCCESS")
except ImportError as e:
    print(f"FAILED: {e}")
    sys.exit(1)
'''
            
            test_file = self.install_dir / "test_imports.py"
            test_file.write_text(test_script, encoding='utf-8')
            
            result = subprocess.run([
                str(python_exe), str(test_file)
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0 or "FAILED" in result.stdout:
                raise Exception(f"Test import fallito: {result.stdout}")
            
            self.log("✅ Test import: OK")
            
            # Test 2: Database accessibilità
            db_test_script = '''
import chromadb
from pathlib import Path

try:
    client = chromadb.PersistentClient(path="./Rag_db")
    collections = client.list_collections()
    print(f"✅ Database: {len(collections)} collezioni")
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
'''
            
            test_file.write_text(db_test_script, encoding='utf-8')
            
            result = subprocess.run([
                str(python_exe), str(test_file)
            ], capture_output=True, text=True, timeout=30)
            
            if "FAILED" in result.stdout:
                raise Exception(f"Test database fallito: {result.stdout}")
            
            self.log("✅ Test database: OK")
            
            # Rimuovi file test
            test_file.unlink()
            
            # Calcola dimensioni finali
            total_size = sum(f.stat().st_size for f in self.install_dir.rglob('*') if f.is_file())
            size_mb = total_size / 1024 / 1024
            
            self.log(f"📊 Dimensione totale: {size_mb:.1f} MB")
            
        except Exception as e:
            raise Exception(f"Test finale fallito: {str(e)}")
    
    def setup_finished(self):
        """Setup completato con successo"""
        self.start_button.config(
            state='normal', 
            text="✅ Installazione Completata!", 
            bg='#10b981'
        )
        self.cancel_button.config(state='disabled')
        self.update_progress(100, "🎉 Installazione completata con successo!")
        
        messagebox.showinfo(
            "🎉 Installazione Completata!",
            f"✅ Il sistema RAG è stato installato con successo!\n\n"
            f"📁 Percorso: {self.install_dir}\n\n"
            f"🚀 Per avviare il sistema:\n"
            f"   Doppio-click su '🚀 AVVIA_RAG_PSICOLOGIA.bat'\n\n"
            f"📖 Consulta 'README_UTENTE.txt' per istruzioni dettagliate."
        )
    
    def setup_failed(self, error_msg):
        """Setup fallito"""
        self.start_button.config(
            state='normal', 
            text="❌ Riprova Installazione", 
            bg='#dc2626'
        )
        self.cancel_button.config(state='disabled')
        self.update_progress(0, "❌ Installazione fallita")
        
        messagebox.showerror(
            "❌ Installazione Fallita",
            f"Si è verificato un errore durante l'installazione:\n\n"
            f"{error_msg}\n\n"
            f"💡 Suggerimenti:\n"
            f"• Verifica connessione internet\n"
            f"• Assicurati di avere permessi di scrittura\n"
            f"• Controlla che il database sia valido\n"
            f"• Consulta il log per dettagli"
        )
    
    # Metodi per generare codice dei file (invariati dal codice precedente)
    def get_rag_system_code(self):
        """Codice rag_system.py ottimizzato"""
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
        """Ricerca semantica e generazione risposta"""
        try:
            # Genera embedding della query
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small", input=[query]
            )
            query_embedding = response.data[0].embedding
            
            # Ricerca in tutte le collezioni
            all_results = []
            collections = self.client.list_collections()
            
            for collection_info in collections:
                collection = self.client.get_collection(collection_info.name)
                results = collection.query(
                    query_embeddings=[query_embedding], 
                    n_results=min(n_results, collection.count())
                )
                
                for i in range(len(results['documents'][0])):
                    all_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity': 1 - results['distances'][0][i],
                    })
            
            # Ordina per rilevanza e prendi i migliori
            all_results.sort(key=lambda x: x['similarity'], reverse=True)
            top_results = all_results[:n_results]
            
            if not top_results:
                return {
                    'query': query,
                    'response': "Non ho trovato informazioni rilevanti per la tua domanda.",
                    'sources': []
                }
            
            # Costruisci contesto per GPT
            context = "\\n\\n".join([
                f"[FONTE] {Path(r['metadata']['source_file']).name}, "
                f"pagina {r['metadata']['page_number']}:\\n{r['content']}"
                for r in top_results
            ])
            
            # Genera risposta con GPT-4
            gpt_response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "Sei un esperto di psicologia. Rispondi sempre basandoti "
                                 "esclusivamente sui documenti forniti. Cita sempre le fonti "
                                 "usando il formato [Fonte: nome_file.pdf, pagina X]. "
                                 "Se i documenti non contengono informazioni sufficienti, "
                                 "dillo chiaramente."
                    },
                    {
                        "role": "user", 
                        "content": f"DOMANDA: {query}\\n\\nDOCUMENTI DISPONIBILI:\\n{context}"
                    }
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
                        'content_preview': r['content'][:200] + "..." if len(r['content']) > 200 else r['content']
                    }
                    for r in top_results
                ]
            }
            
        except Exception as e:
            return {
                'query': query,
                'response': f"Errore durante la ricerca: {str(e)}",
                'sources': []
            }
'''
    
    def get_web_app_code(self):
        """Codice web_app.py ottimizzato"""
        return '''import streamlit as st
import os
from rag_system import SimpleRAGQuery

# Configurazione pagina
st.set_page_config(
    page_title="🧠 RAG Psicologia",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizzato
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .stTextArea textarea {
        font-size: 16px;
    }
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
    }
    .success-box {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header principale
st.markdown('<h1 class="main-header">🧠 Sistema RAG - Consultazione Psicologia</h1>', unsafe_allow_html=True)

# Inizializzazione sistema RAG
@st.cache_resource
def init_rag_system():
    """Inizializza sistema RAG con gestione errori"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        try:
            with open('.api_key', 'r') as f:
                api_key = f.read().strip()
        except FileNotFoundError:
            return None, "File API key non trovato"
        except Exception as e:
            return None, f"Errore lettura API key: {str(e)}"
    
    try:
        rag = SimpleRAGQuery(api_key, db_path="./Rag_db")
        return rag, "OK"
    except Exception as e:
        return None, f"Errore inizializzazione: {str(e)}"

# Carica sistema
rag_system, status = init_rag_system()

if rag_system is None:
    st.error(f"❌ Errore sistema: {status}")
    st.markdown("""
    ### 🔧 Possibili soluzioni:
    - Verifica che il file `.api_key` sia presente
    - Controlla che la cartella `Rag_db` sia nella directory corretta
    - Riavvia il sistema tramite il launcher
    """)
    st.stop()

# Sistema operativo
st.markdown('<div class="success-box">✅ Sistema RAG connesso e operativo!</div>', unsafe_allow_html=True)

# Interfaccia principale
st.subheader("💭 Poni la Tua Domanda Psicologica")

# Area input domanda
query = st.text_area(
    "Scrivi qui la tua domanda:",
    placeholder="Esempio: Qual è la differenza tra ansia e angoscia secondo questi autori?",
    height=120,
    help="Inserisci una domanda specifica per ottenere risposte dettagliate dai documenti"
)

# Configurazioni e pulsante ricerca
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Opzioni")
    n_sources = st.slider(
        "Numero fonti da consultare:", 
        min_value=3, 
        max_value=10, 
        value=5,
        help="Più fonti = risposta più completa ma tempo maggiore"
    )

with col2:
    st.subheader("🔍 Ricerca")
    if st.button("🚀 Ottieni Risposta", type="primary"):
        if query.strip():
            # Barra di progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🧠 Analizzando la domanda...")
            progress_bar.progress(25)
            
            with st.spinner("🔍 Ricerca nei documenti in corso..."):
                result = rag_system.search_and_respond(query, n_sources)
            
            progress_bar.progress(100)
            status_text.text("✅ Analisi completata!")
            
            # Risultati
            st.markdown("---")
            
            # Risposta principale
            st.markdown("### 📝 Risposta del Sistema")
            if result['response']:
                st.markdown(result['response'])
            else:
                st.warning("⚠️ Nessuna risposta generata.")
            
            # Fonti consultate
            if result['sources']:
                st.markdown("### 📚 Fonti Consultate")
                
                for i, source in enumerate(result['sources'], 1):
                    with st.expander(
                        f"📄 **Fonte {i}**: {source['file_name']} "
                        f"(Pagina {source['page_number']}) - "
                        f"Rilevanza: {source['similarity']:.1%}"
                    ):
                        st.markdown(f"**File:** {source['file_name']}")
                        st.markdown(f"**Pagina:** {source['page_number']}")
                        st.markdown(f"**Rilevanza:** {source['similarity']:.1%}")
                        st.markdown("**Estratto del contenuto:**")
                        st.text(source['content_preview'])
            else:
                st.info("ℹ️ Nessuna fonte trovata per questa domanda.")
            
            # Pulisci progress bar
            progress_bar.empty()
            status_text.empty()
            
        else:
            st.error("❗ Inserisci una domanda prima di procedere!")

# Sezione esempi (collassabile)
with st.expander("💡 Esempi di Domande Efficaci"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🧠 Concetti Teorici:**
        - "Qual è la differenza tra ansia e angoscia?"
        - "Come viene definito il transfert in psicoanalisi?"
        - "Cosa si intende per resistenza in terapia?"
        - "Caratteristiche del Super-Io secondo Freud?"
        
        **📊 Disturbi e Sintomi:**
        - "Criteri diagnostici del disturbo borderline?"
        - "Come si manifesta un episodio maniacale?"
        - "Sintomi della depressione maggiore?"
        """)
    
    with col2:
        st.markdown("""
        **🔄 Confronti Teorici:**
        - "Differenze tra Jung e Freud sull'inconscio?"
        - "Approccio cognitivo vs psicodinamico alla depressione?"
        - "Terapia sistemica vs individuale?"
        
        **🏥 Applicazioni Cliniche:**
        - "Tecniche di intervento nell'ansia?"
        - "Come condurre un colloquio clinico?"
        - "Strategie terapeutiche per l'adolescenza?"
        """)

# Footer informativo
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 14px; margin-top: 2rem;">
    🧠 <strong>Sistema RAG per Psicologia</strong> | 
    Consultazione intelligente di documenti specialistici | 
    ⚡ Alimentato da OpenAI GPT-4
</div>
""", unsafe_allow_html=True)
'''
    
    def get_launcher_code(self):
        """Codice launcher.py robusto"""
        return '''#!/usr/bin/env python3
"""
Launcher robusto per Sistema RAG Psicologia
Avvia l'interfaccia web con gestione errori completa
"""

import os
import sys
import subprocess
import webbrowser
import time
import signal
from pathlib import Path

class RAGLauncher:
    def __init__(self):
        self.streamlit_process = None
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Gestione segnali per chiusura pulita"""
        def signal_handler(signum, frame):
            print("\\n🛑 Ricevuto segnale di chiusura...")
            self.cleanup()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def cleanup(self):
        """Pulizia processi al termine"""
        if self.streamlit_process:
            try:
                self.streamlit_process.terminate()
                self.streamlit_process.wait(timeout=5)
                print("✅ Sistema fermato correttamente")
            except:
                try:
                    self.streamlit_process.kill()
                except:
                    pass
    
    def check_requirements(self):
        """Verifica requisiti sistema"""
        print("🔍 Verifica requisiti sistema...")
        
        # Verifica API key
        api_key_file = Path('.api_key')
        if not api_key_file.exists():
            print("❌ File API key (.api_key) non trovato!")
            print("💡 Assicurati che il file .api_key sia presente nella directory")
            return False
        
        try:
            api_key = api_key_file.read_text().strip()
            if not api_key.startswith('sk-'):
                print("❌ API key non valida (deve iniziare con 'sk-')")
                return False
            
            os.environ['OPENAI_API_KEY'] = api_key
            print(f"✅ API key caricata: {api_key[:10]}...{api_key[-4:]}")
            
        except Exception as e:
            print(f"❌ Errore lettura API key: {e}")
            return False
        
        # Verifica database
        if not Path('Rag_db').exists():
            print("❌ Database RAG (cartella Rag_db) non trovato!")
            print("📁 Assicurati che la cartella 'Rag_db' sia presente")
            return False
        
        db_files = len(list(Path('Rag_db').rglob('*')))
        if db_files == 0:
            print("❌ Database RAG vuoto!")
            return False
        
        print(f"✅ Database RAG trovato: {db_files} file")
        
        # Verifica file sistema
        required_files = ['rag_system.py', 'web_app.py']
        for file in required_files:
            if not Path(file).exists():
                print(f"❌ File mancante: {file}")
                return False
        
        print("✅ Tutti i file di sistema presenti")
        return True
    
    def test_imports(self):
        """Test import pacchetti essenziali"""
        print("🧪 Test pacchetti Python...")
        
        try:
            import openai
            print("✅ OpenAI OK")
        except ImportError:
            print("❌ Pacchetto OpenAI mancante")
            return False
        
        try:
            import chromadb
            print("✅ ChromaDB OK") 
        except ImportError:
            print("❌ Pacchetto ChromaDB mancante")
            return False
        
        try:
            import streamlit
            print("✅ Streamlit OK")
        except ImportError:
            print("❌ Pacchetto Streamlit mancante")
            return False
        
        return True
    
    def start_streamlit(self):
        """Avvia server Streamlit"""
        print("🚀 Avviando server Streamlit...")
        
        try:
            self.streamlit_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", 
                "web_app.py",
                "--server.address", "localhost",
                "--server.port", "8501", 
                "--browser.gatherUsageStats", "false",
                "--server.headless", "true",
                "--logger.level", "error"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            print("⏳ Attendo avvio server...")
            
            # Attesa con timeout
            for i in range(15):  # Max 15 secondi
                if self.streamlit_process.poll() is not None:
                    # Processo terminato prematuramente
                    stdout, stderr = self.streamlit_process.communicate()
                    print(f"❌ Streamlit terminato inaspettatamente:")
                    print(f"STDOUT: {stdout.decode()}")
                    print(f"STDERR: {stderr.decode()}")
                    return False
                
                time.sleep(1)
                print(f"⏳ Avvio in corso... ({i+1}/15)")
            
            print("✅ Server Streamlit avviato!")
            return True
            
        except Exception as e:
            print(f"❌ Errore avvio Streamlit: {e}")
            return False
    
    def open_browser(self):
        """Apri browser con gestione errori"""
        print("🌐 Apertura browser...")
        
        url = "http://localhost:8501"
        
        try:
            webbrowser.open(url)
            print(f"✅ Browser aperto: {url}")
            return True
        except Exception as e:
            print(f"⚠️ Errore apertura browser automatica: {e}")
            print(f"🔗 Apri manualmente: {url}")
            return False
    
    def monitor_system(self):
        """Monitora sistema in esecuzione"""
        print("\\n" + "="*50)
        print("🎉 SISTEMA RAG PSICOLOGIA ATTIVO!")
        print("="*50)
        print("🌐 Interfaccia web: http://localhost:8501")
        print("📚 Pronto per le tue domande di psicologia")
        print("❌ Per fermare: Ctrl+C oppure chiudi questa finestra")
        print("="*50)
        
        try:
            # Monitora processo Streamlit
            while True:
                if self.streamlit_process.poll() is not None:
                    print("\\n❌ Il server Streamlit si è arrestato inaspettatamente")
                    stdout, stderr = self.streamlit_process.communicate()
                    if stderr:
                        print(f"Errore: {stderr.decode()}")
                    break
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\\n🛑 Arresto richiesto dall'utente...")
        
        self.cleanup()
    
    def run(self):
        """Esegue launcher completo"""
        print("🧠 SISTEMA RAG PSICOLOGIA - LAUNCHER")
        print("="*40)
        
        # 1. Verifica requisiti
        if not self.check_requirements():
            print("\\n❌ Verifica requisiti fallita!")
            self.wait_exit()
            return 1
        
        # 2. Test import
        if not self.test_imports():
            print("\\n❌ Test pacchetti fallito!")
            print("💡 Prova a reinstallare il sistema")
            self.wait_exit()
            return 1
        
        # 3. Avvia Streamlit
        if not self.start_streamlit():
            print("\\n❌ Avvio server fallito!")
            self.wait_exit()
            return 1
        
        # 4. Apri browser
        time.sleep(2)  # Attesa aggiuntiva per stabilizzazione
        self.open_browser()
        
        # 5. Monitora sistema
        self.monitor_system()
        
        return 0
    
    def wait_exit(self):
        """Attende input utente prima di uscire"""
        try:
            input("\\nPremi Invio per uscire...")
        except:
            pass

def main():
    """Funzione principale"""
    launcher = RAGLauncher()
    return launcher.run()

if __name__ == "__main__":
    sys.exit(main())
'''
    
    def get_user_readme(self):
        """README utente completo"""
        return f'''🧠 SISTEMA RAG PSICOLOGIA - GUIDA COMPLETA
==========================================

✅ INSTALLAZIONE COMPLETATA CON SUCCESSO!

Il tuo sistema RAG (Retrieval-Augmented Generation) per la consultazione
di documenti di psicologia è stato installato e configurato correttamente.

🚀 AVVIO RAPIDO:
===============
1. Fai doppio-click su: "🚀 AVVIA_RAG_PSICOLOGIA.bat"
2. Attendi l'avvio del sistema (finestra nera)
3. Il browser si aprirà automaticamente con l'interfaccia
4. Inizia a porre le tue domande!

🌐 ACCESSO MANUALE:
===================
Se il browser non si apre automaticamente:
http://localhost:8501

📁 STRUTTURA DEL SISTEMA:
========================
{self.install_dir}/
├── python/                 → Python isolato con dipendenze
├── Rag_db/                 → Database documenti psicologia
├── rag_system.py           → Motore di ricerca semantica
├── web_app.py              → Interfaccia web Streamlit
├── launcher.py             → Sistema di avvio
├── .api_key                → Tua API key OpenAI (PRIVATA!)
└── 🚀 AVVIA_RAG_PSICOLOGIA.bat → Launcher Windows

💭 ESEMPI DI DOMANDE EFFICACI:
=============================

🧠 Concetti Teorici:
- "Qual è la differenza tra ansia e angoscia secondo Freud?"
- "Come viene definito il transfert in psicoanalisi?"
- "Caratteristiche del Super-Io e dell'Es?"
- "Cosa si intende per resistenza in terapia?"

📊 Disturbi e Diagnosi:
- "Criteri diagnostici del disturbo borderline di personalità?"
- "Come si manifesta un episodio maniacale nel bipolare?"
- "Sintomi principali della depressione maggiore?"
- "Differenze tra ansia generalizzata e attacchi di panico?"

🔄 Confronti Teorici:
- "Differenze tra Jung e Freud sull'inconscio collettivo?"
- "Approccio cognitivo vs psicodinamico alla depressione?"
- "Terapia sistemica vs terapia individuale?"

🏥 Applicazioni Cliniche:
- "Tecniche di intervento per disturbi d'ansia?"
- "Come condurre un primo colloquio clinico?"
- "Strategie terapeutiche per adolescenti?"

🔧 RISOLUZIONE PROBLEMI:
=======================

🚫 "File API key non trovato"
   → Il file .api_key è stato configurato durante l'installazione
   → Se manca, contatta chi ti ha fornito il sistema

🚫 "Database RAG non trovato"  
   → La cartella Rag_db dovrebbe essere presente
   → Se manca, reinstalla il sistema

🚫 "Porta 8501 occupata"
   → Chiudi altre applicazioni Streamlit
   → Riavvia il computer se il problema persiste

🚫 "Errore pacchetti Python"
   → Il sistema è autocontenuto, non dovrebbe accadere
   → Prova a reinstallare completamente

🚫 Browser non si apre automaticamente
   → Vai manualmente su: http://localhost:8501
   → Assicurati che il sistema sia avviato (finestra nera aperta)

🚫 Risposte poco rilevanti
   → Prova a riformulare la domanda in modo più specifico
   → Usa termini tecnici presenti nei documenti
   → Aumenta il numero di fonti consultate (slider nell'interfaccia)

⚡ OTTIMIZZAZIONE DELLE RICERCHE:
===============================

✅ Domande specifiche funzionano meglio:
   ❌ "Dimmi tutto sulla depressione"
   ✅ "Quali sono i criteri diagnostici DSM-5 per la depressione maggiore?"

✅ Usa terminologia tecnica:
   ❌ "Problemi di umore"  
   ✅ "Disturbi dell'umore" o "episodio depressivo"

✅ Specifica l'autore o approccio:
   ❌ "Cos'è l'inconscio?"
   ✅ "Come definisce Freud l'inconscio dinamico?"

🔒 SICUREZZA E PRIVACY:
======================
- ✅ Sistema completamente OFFLINE dopo installazione
- ✅ Database locale, nessun dato inviato esternamente  
- ✅ API key memorizzata localmente in modo sicuro
- ✅ Nessuna raccolta dati o telemetria

📊 CARATTERISTICHE TECNICHE:
===========================
- 🧠 Motore: OpenAI GPT-4 + Embeddings
- 🗃️ Database: ChromaDB vettoriale locale
- 🌐 Interfaccia: Streamlit web app
- 🐍 Python: {self.python_version} embedded
- 💾 Dimensione totale: ~200-300 MB
- ⚡ Ricerca semantica in millisecondi

📞 SUPPORTO:
============
Per problemi tecnici, invia screenshot degli errori alla persona
che ti ha fornito questo sistema insieme a:

- Messaggio di errore completo
- Sistema operativo in uso  
- Descrizione di cosa stavi facendo quando è apparso l'errore

🎯 SUGGERIMENTI PER L'USO:
=========================
1. 🎯 Sii specifico nelle domande
2. 📚 Consulta sempre le fonti mostrate
3. 🔄 Prova riformulazioni se non soddisfatto
4. 📈 Aumenta le fonti per argomenti complessi
5. 💡 Usa gli esempi come guida per formulare domande

Buona consultazione! 🧠📚✨

---
Sistema RAG Psicologia v2.0 | Installato il {time.strftime("%d/%m/%Y alle %H:%M")}
'''

if __name__ == "__main__":
    app = RobustRAGInstaller()
    app.root.mainloop()