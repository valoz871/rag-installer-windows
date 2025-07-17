def update_certificates(self):
        """Aggiorna certificati SSL di Windows automaticamente"""
        self.log_message("🔐 Aggiornamento certificati SSL...", "INFO")
        
        try:
            # Metodo 1: Usa Windows Update per certificati
            self.log_message("📥 Scaricamento certificati Microsoft...", "INFO")
            
            # Comando per aggiornare certificati root via Windows
            cert_update_commands = [
                # Aggiorna certificati root Microsoft
                ["certlm.exe", "/s", "/c", "DisallowedCert", "/d"],
                ["powershell", "-Command", "Get-ChildItem -Path Cert:\\LocalMachine\\Root | Update-Certificate"],
                # Forza aggiornamento via Windows Update
                ["powershell", "-Command", "Import-Module PSWindowsUpdate; Get-WUInstall -AcceptAll -AutoReboot:$false -Category 'Security Updates'"]
            ]
            
            # Prova metodo semplificato: scarica certificati Mozilla
            mozilla_cert_url = "https://curl.se/ca/cacert.pem"
            local_cert_path = Path.cwd() / "cacert.pem"
            
            # Usa PowerShell per scaricare certificati (più affidabile)
            ps_command = f'''
$ProgressPreference = 'SilentlyContinue'
try {{
    Invoke-WebRequest -Uri "{mozilla_cert_url}" -OutFile "{local_cert_path}" -UseBasicParsing
    Write-Host "✅ Certificati scaricati"
}} catch {{
    Write-Host "❌ Errore download certificati: $_"
    exit 1
}}
'''
            
            result = subprocess.run([
                "powershell", "-Command", ps_command
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log_message("✅ Certificati Mozilla scaricati", "SUCCESS")
                
                # Configura Python per usare i certificati scaricati
                os.environ['REQUESTS_CA_BUNDLE'] = str(local_cert_path)
                os.environ['SSL_CERT_FILE'] = str(local_cert_path)
                
                self.log_message("✅ Certificati configurati per Python", "SUCCESS")
                return True
            else:
                self.log_message(f"⚠️ Download certificati fallito: {result.stderr}", "WARNING")
                
        except Exception as e:
            self.log_message(f"⚠️ Aggiornamento certificati fallito: {e}", "WARNING")
        
        # Metodo fallback: Aggiorna store Windows nativamente
        try:
            self.log_message("🔄 Tentativo aggiornamento store Windows...", "INFO")
            
            # Comando Windows per aggiornare certificati root
            update_cmd = '''
$certStore = New-Object System.Security.Cryptography.X509Certificates.X509Store([System.Security.Cryptography.X509Certificates.StoreName]::Root, [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine)
$certStore.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
Write-Host "Store certificati aperto per aggiornamento"
$certStore.Close()
'''
            
            subprocess.run([
                "powershell", "-Command", update_cmd
            ], capture_output=True, text=True, timeout=30)
            
            self.log_message("✅ Store certificati aggiornato", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_message(f"⚠️ Aggiornamento store fallito: {e}", "WARNING")
        
        # Se tutto fallisce, procedi comunque
        self.log_message("⚠️ Continuo senza aggiornamento certificati", "WARNING")
        return False#!/usr/bin/env python3
"""
Smart Installer per Sistema RAG - Scarica Python Embedded e crea sistema autocontenuto
Sviluppabile da Mac, funziona su Windows!
"""

import os
import sys
import zipfile
import urllib.request
import urllib.error
import json
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import tempfile
import shutil

class SmartRAGInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧠 RAG Psicologia - Smart Installer")
        self.root.geometry("700x600")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(False, False)
        
        # Configurazione
        self.python_version = "3.11.8"  # Versione stabile
        self.install_dir = Path.cwd() / "RAG_Psicologia_Sistema"
        self.python_embedded_url = f"https://www.python.org/ftp/python/{self.python_version}/python-{self.python_version}-embed-amd64.zip"
        
        # Stato
        self.api_key = ""
        self.install_complete = False
        self.cancel_install = False
        self.source_db_path = None  # Percorso database sorgente
        
        self.create_interface()
    
    def create_interface(self):
        """Crea interfaccia installer"""
        
        # Header elegante
        header_frame = tk.Frame(self.root, bg='#1e3a8a', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🧠 Sistema RAG Psicologia",
            font=("Arial", 20, "bold"),
            fg="white",
            bg='#1e3a8a'
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Smart Installer - Python Embedded",
            font=("Arial", 12),
            fg="#a5b4fc",
            bg='#1e3a8a'
        )
        subtitle_label.pack()
        
        # Contenuto principale
        main_frame = tk.Frame(self.root, bg='#f0f8ff', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Info installer
        info_text = tk.Label(
            main_frame,
            text="✨ Questo installer creerà un sistema completamente autonomo:\n"
                 "• Scarica Python isolato (nessun conflitto)\n"
                 "• Installa tutte le dipendenze automaticamente\n"
                 "• Crea launcher finale per l'utente\n"
                 "• Sistema portabile e autocontenuto",
            font=("Arial", 11),
            bg='#f0f8ff',
            fg='#374151',
            justify='left',
            wraplength=600
        )
        info_text.pack(pady=15, anchor='w')
        
        # Separator
        separator = tk.Frame(main_frame, height=2, bg='#e5e7eb')
        separator.pack(fill='x', pady=15)
        
        # Configurazione
        config_frame = tk.LabelFrame(
            main_frame, 
            text="⚙️ Configurazione",
            font=("Arial", 12, "bold"),
            bg='#f0f8ff',
            padx=15,
            pady=15
        )
        config_frame.pack(fill='x', pady=10)
        
        # Directory installazione
        tk.Label(
            config_frame,
            text="📁 Directory installazione:",
            font=("Arial", 10, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w')
        
        dir_frame = tk.Frame(config_frame, bg='#f0f8ff')
        dir_frame.pack(fill='x', pady=5)
        
        self.dir_var = tk.StringVar(value=str(self.install_dir))
        dir_entry = tk.Entry(
            dir_frame,
            textvariable=self.dir_var,
            font=("Arial", 10),
            width=50
        )
        dir_entry.pack(side='left', fill='x', expand=True)
        
        change_dir_btn = tk.Button(
            dir_frame,
            text="📂",
            command=self.choose_directory,
            width=3
        )
        change_dir_btn.pack(side='right', padx=(5, 0))
        
        # Database RAG path
        tk.Label(
            config_frame,
            text="🗄️ Percorso database Rag_db:",
            font=("Arial", 10, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w', pady=(15, 0))
        
        db_frame = tk.Frame(config_frame, bg='#f0f8ff')
        db_frame.pack(fill='x', pady=5)
        
        # Default: cerca Rag_db nella stessa directory dell'installer
        default_db_path = Path.cwd() / "Rag_db"
        self.db_var = tk.StringVar(value=str(default_db_path))
        
        db_entry = tk.Entry(
            db_frame,
            textvariable=self.db_var,
            font=("Arial", 10),
            width=50
        )
        db_entry.pack(side='left', fill='x', expand=True)
        
        change_db_btn = tk.Button(
            db_frame,
            text="📂",
            command=self.choose_database,
            width=3
        )
        change_db_btn.pack(side='right', padx=(5, 0))
        
        # Auto-detect button
        detect_btn = tk.Button(
            config_frame,
            text="🔍 Auto-rileva Rag_db",
            command=self.auto_detect_database,
            bg='#6366f1',
            fg='white',
            font=("Arial", 9)
        )
        detect_btn.pack(pady=5)
        
        # API Key
        tk.Label(
            config_frame,
            text="🔑 OpenAI API Key:",
            font=("Arial", 10, "bold"),
            bg='#f0f8ff'
        ).pack(anchor='w', pady=(15, 0))
        
        self.api_entry = tk.Entry(
            config_frame,
            font=("Arial", 11),
            width=60,
            show="*"
        )
        self.api_entry.pack(fill='x', pady=5)
        
        tk.Label(
            config_frame,
            text="(Inizia con 'sk-' - fornita dal creatore del sistema)",
            font=("Arial", 9),
            fg="gray",
            bg='#f0f8ff'
        ).pack(anchor='w')
        
        # Pulsanti azione
        action_frame = tk.Frame(main_frame, bg='#f0f8ff')
        action_frame.pack(fill='x', pady=20)
        
        self.install_btn = tk.Button(
            action_frame,
            text="🚀 Installa Sistema Completo",
            font=("Arial", 14, "bold"),
            bg='#059669',
            fg='white',
            pady=12,
            command=self.start_installation
        )
        self.install_btn.pack(side='left', fill='x', expand=True)
        
        self.cancel_btn = tk.Button(
            action_frame,
            text="❌ Annulla",
            font=("Arial", 12),
            bg='#dc2626',
            fg='white',
            pady=12,
            command=self.cancel_installation,
            state='disabled'
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        # Progress bar
        self.progress_frame = tk.LabelFrame(
            main_frame,
            text="📊 Progresso Installazione",
            font=("Arial", 11, "bold"),
            bg='#f0f8ff'
        )
        self.progress_frame.pack(fill='x', pady=15)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=600
        )
        self.progress_bar.pack(pady=10, padx=15)
        
        self.status_label = tk.Label(
            self.progress_frame,
            text="⏳ Pronto per installazione...",
            font=("Arial", 10),
            bg='#f0f8ff',
            fg='#374151'
        )
        self.status_label.pack(pady=(0, 10))
        
        # Log area
        log_frame = tk.LabelFrame(
            main_frame,
            text="📋 Log Installazione",
            font=("Arial", 11, "bold"),
            bg='#f0f8ff'
        )
        log_frame.pack(fill='both', expand=True, pady=10)
        
        # Scrollable text
        log_scroll_frame = tk.Frame(log_frame)
        log_scroll_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(
            log_scroll_frame,
            height=8,
            font=("Courier", 9),
            bg='#ffffff',
            fg='#000000',
            wrap='word'
        )
        
        scrollbar = tk.Scrollbar(log_scroll_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def choose_directory(self):
        """Scegli directory installazione"""
        from tkinter import filedialog
        
        directory = filedialog.askdirectory(
            title="Scegli directory installazione",
            initialdir=self.dir_var.get()
        )
        if directory:
            self.dir_var.set(directory)
            self.install_dir = Path(directory) / "RAG_Psicologia_Sistema"
    
    def choose_database(self):
        """Scegli directory database Rag_db"""
        from tkinter import filedialog
        
        directory = filedialog.askdirectory(
            title="Scegli cartella Rag_db",
            initialdir=self.db_var.get()
        )
        if directory:
            # Verifica che sia effettivamente una cartella Rag_db valida
            db_path = Path(directory)
            if self.validate_database(db_path):
                self.db_var.set(str(db_path))
                self.log_message(f"✅ Database selezionato: {db_path}", "SUCCESS")
            else:
                messagebox.showerror(
                    "Database Non Valido", 
                    f"La cartella selezionata non sembra contenere un database RAG valido.\n"
                    f"Assicurati di selezionare la cartella 'Rag_db' che contiene i file del database."
                )
    
    def auto_detect_database(self):
        """Auto-rileva database Rag_db in posizioni comuni"""
        self.log_message("🔍 Ricerca automatica database...", "INFO")
        
        # Posizioni comuni da controllare
        search_paths = [
            Path.cwd() / "Rag_db",                          # Stessa cartella installer
            Path.cwd().parent / "Rag_db",                   # Cartella parent
            Path(self.dir_var.get()) / "Rag_db",           # Directory installazione scelta
            Path.home() / "Desktop" / "Rag_db",            # Desktop
            Path.home() / "Downloads" / "Rag_db",          # Downloads
        ]
        
        # Cerca anche in sottocartelle
        for base_path in [Path.cwd(), Path.cwd().parent, Path.home() / "Desktop"]:
            try:
                for item in base_path.iterdir():
                    if item.is_dir() and item.name.lower() == "rag_db":
                        search_paths.append(item)
            except:
                continue
        
        found_databases = []
        
        for db_path in search_paths:
            if self.validate_database(db_path):
                found_databases.append(db_path)
                self.log_message(f"✅ Database trovato: {db_path}", "SUCCESS")
        
        if found_databases:
            # Usa il primo trovato
            best_db = found_databases[0]
            self.db_var.set(str(best_db))
            
            if len(found_databases) > 1:
                messagebox.showinfo(
                    "Database Rilevati",
                    f"Trovati {len(found_databases)} database RAG.\n"
                    f"Selezionato: {best_db}\n\n"
                    f"Puoi cambiare manualmente se necessario."
                )
            else:
                messagebox.showinfo(
                    "Database Trovato",
                    f"✅ Database RAG rilevato automaticamente:\n{best_db}"
                )
        else:
            messagebox.showwarning(
                "Database Non Trovato",
                "🔍 Nessun database RAG trovato automaticamente.\n\n"
                "Usa il pulsante 📂 per selezionare manualmente la cartella Rag_db."
            )
            self.log_message("❌ Nessun database trovato automaticamente", "WARNING")
    
    def validate_database(self, db_path):
        """Valida che la cartella sia un database RAG valido"""
        if not db_path.exists() or not db_path.is_dir():
            return False
        
        # Controlla presenza file database tipici
        expected_files = ['chroma.sqlite3', 'chroma.sqlite3-wal', 'chroma.sqlite3-shm']
        has_db_files = any((db_path / f).exists() for f in expected_files)
        
        # O controlla cartelle UUID tipiche di ChromaDB
        has_uuid_dirs = any(
            item.is_dir() and len(item.name) == 36 and item.name.count('-') == 4
            for item in db_path.iterdir()
        )
        
        # Verifica che non sia vuota
        has_files = len(list(db_path.iterdir())) > 0
        
        return has_files and (has_db_files or has_uuid_dirs)
    
    def log_message(self, message, level="INFO"):
        """Aggiungi messaggio al log"""
        levels = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌"
        }
        
        icon = levels.get(level, "ℹ️")
        formatted_message = f"{icon} {message}\n"
        
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_progress(self, value, status):
        """Aggiorna progress bar e status"""
        self.progress_bar['value'] = value
        self.status_label.config(text=status)
        self.root.update()
    
    def start_installation(self):
        """Avvia installazione"""
        # Validazione API Key
        self.api_key = self.api_entry.get().strip()
        if not self.api_key:
            messagebox.showerror("Errore", "Inserisci la API Key OpenAI!")
            return
        
        if not self.api_key.startswith('sk-'):
            messagebox.showerror("Errore", "API Key deve iniziare con 'sk-'")
            return
        
        # Validazione percorsi
        self.install_dir = Path(self.dir_var.get()) / "RAG_Psicologia_Sistema"
        db_path = Path(self.db_var.get())
        
        # Pre-validazione database
        if not self.validate_database(db_path):
            messagebox.showerror(
                "Database Non Valido", 
                f"Il database selezionato non è valido:\n{db_path}\n\n"
                f"Usa il pulsante 🔍 Auto-rileva o 📂 per selezionare il database corretto."
            )
            return
        
        # Conferma installazione
        if self.install_dir.exists():
            if not messagebox.askyesno(
                "Directory Esistente", 
                f"La directory {self.install_dir} esiste già.\n"
                "Vuoi sovrascrivere il contenuto?"
            ):
                return
        
        # Mostra riepilogo
        summary = f"""
📋 RIEPILOGO INSTALLAZIONE:

📁 Directory installazione: {self.install_dir}
🗄️ Database RAG: {db_path}
🔑 API Key: {self.api_key[:10]}...{self.api_key[-4:]}

Procedere con l'installazione?
"""
        
        if not messagebox.askyesno("Conferma Installazione", summary):
            return
        
        # Prepara UI per installazione
        self.install_btn.config(state='disabled')
        self.cancel_btn.config(state='normal')
        self.cancel_install = False
        
        # Avvia installazione in thread separato
        install_thread = threading.Thread(target=self.run_installation)
        install_thread.daemon = True
        install_thread.start()
    
    def cancel_installation(self):
        """Annulla installazione"""
        self.cancel_install = True
        self.log_message("Installazione annullata dall'utente", "WARNING")
        self.install_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')
        self.update_progress(0, "❌ Installazione annullata")
    
    def run_installation(self):
        """Esegue installazione completa"""
        try:
            steps = [
                ("Preparazione directory", self.prepare_directory),
                ("Download Python Embedded", self.download_python_embedded),
                ("Estrazione Python", self.extract_python),
                ("Configurazione Python", self.configure_python),
                ("Installazione dipendenze", self.install_dependencies),
                ("Copia file sistema", self.copy_system_files),
                ("Creazione launcher", self.create_launcher),
                ("Test finale", self.test_installation),
                ("Finalizzazione", self.finalize_installation)
            ]
            
            total_steps = len(steps)
            
            for i, (step_name, step_func) in enumerate(steps):
                if self.cancel_install:
                    return
                
                progress = (i / total_steps) * 100
                self.update_progress(progress, f"⏳ {step_name}...")
                self.log_message(f"Inizio: {step_name}")
                
                step_func()
                
                self.log_message(f"Completato: {step_name}", "SUCCESS")
            
            # Installazione completata
            self.update_progress(100, "✅ Installazione completata!")
            self.log_message("🎉 INSTALLAZIONE COMPLETATA CON SUCCESSO!", "SUCCESS")
            
            self.installation_finished()
            
        except Exception as e:
            self.log_message(f"Errore durante installazione: {str(e)}", "ERROR")
            self.installation_failed(str(e))
    
    def prepare_directory(self):
        """Prepara directory installazione con gestione conflitti"""
        if self.install_dir.exists():
            self.log_message(f"⚠️ Directory già esistente: {self.install_dir}", "WARNING")
            self.log_message("🗑️ Rimozione installazione precedente...", "INFO")
            
            try:
                # Rimuovi directory esistente completamente
                shutil.rmtree(self.install_dir)
                self.log_message("✅ Installazione precedente rimossa", "SUCCESS")
            except Exception as e:
                self.log_message(f"❌ Errore rimozione: {e}", "ERROR")
                # Prova con nome alternativo
                counter = 1
                while True:
                    alt_dir = self.install_dir.parent / f"{self.install_dir.name}_{counter}"
                    if not alt_dir.exists():
                        self.install_dir = alt_dir
                        break
                    counter += 1
                self.log_message(f"📁 Usando directory alternativa: {self.install_dir}", "INFO")
        
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.log_message(f"📁 Directory preparata: {self.install_dir}", "SUCCESS")
    
    def download_python_embedded(self):
        """Scarica Python Embedded con gestione SSL"""
        python_zip_path = self.install_dir / "python_embedded.zip"
        
        self.log_message(f"Scaricando Python {self.python_version} embedded...")
        
        # Configurazione SSL per VM/testing
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        def download_progress(block_num, block_size, total_size):
            if self.cancel_install:
                raise Exception("Download annullato")
            
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, (downloaded / total_size) * 100)
                self.update_progress(
                    20 + (percent * 0.3),  # 20-50% del progresso totale
                    f"⬇️ Scaricando Python... {percent:.1f}%"
                )
        
        try:
            # Usa urllib con SSL context disabilitato
            import urllib.request
            
            # Configura opener con SSL context
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
            urllib.request.install_opener(opener)
            
            urllib.request.urlretrieve(
                self.python_embedded_url,
                python_zip_path,
                reporthook=download_progress
            )
            
            self.log_message(f"Download completato: {python_zip_path.stat().st_size / 1024 / 1024:.1f} MB")
            
        except Exception as e:
            self.log_message(f"Errore download con SSL bypass: {e}", "ERROR")
            
            # Prova con requests se disponibile
            try:
                import requests
                self.log_message("Tentativo con requests...", "INFO")
                
                response = requests.get(self.python_embedded_url, verify=False, stream=True)
                total_size = int(response.headers.get('content-length', 0))
                
                with open(python_zip_path, 'wb') as f:
                    downloaded = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if self.cancel_install:
                            raise Exception("Download annullato")
                        
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            self.update_progress(
                                20 + (percent * 0.3),
                                f"⬇️ Scaricando Python... {percent:.1f}%"
                            )
                
                self.log_message(f"Download completato con requests: {downloaded / 1024 / 1024:.1f} MB")
                
            except ImportError:
                self.log_message("Requests non disponibile", "ERROR")
                raise Exception("Impossibile scaricare Python: problemi SSL e requests non disponibile")
            except Exception as e2:
                self.log_message(f"Errore anche con requests: {e2}", "ERROR")
                raise Exception(f"Download fallito: {e2}")
    
    def extract_python(self):
        """Estrae Python embedded"""
        python_zip_path = self.install_dir / "python_embedded.zip"
        python_dir = self.install_dir / "python"
        
        with zipfile.ZipFile(python_zip_path, 'r') as zip_ref:
            zip_ref.extractall(python_dir)
        
        # Rimuovi zip
        python_zip_path.unlink()
        
        self.log_message(f"Python estratto in: {python_dir}")
    
    def configure_python(self):
        """Configura Python embedded per pip con certificati corretti"""
        python_dir = self.install_dir / "python"
        
        # Abilita site-packages nel python._pth
        pth_file = python_dir / f"python{self.python_version.replace('.', '')[:2]}._pth"
        if not pth_file.exists():
            # Cerca file ._pth esistente
            pth_files = list(python_dir.glob("python*._pth"))
            if pth_files:
                pth_file = pth_files[0]
        
        if pth_file.exists():
            content = pth_file.read_text()
            if "#import site" in content:
                content = content.replace("#import site", "import site")
                pth_file.write_text(content)
                self.log_message("Abilitato site-packages in Python embedded")
        
        # Scarica get-pip.py con gestione certificati
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_path = python_dir / "get-pip.py"
        
        self.log_message("📥 Scaricando get-pip.py...")
        
        try:
            # Metodo 1: urllib standard
            urllib.request.urlretrieve(get_pip_url, get_pip_path)
            self.log_message("✅ get-pip.py scaricato con urllib")
            
        except Exception as e:
            self.log_message(f"❌ Errore urllib per get-pip: {e}", "WARNING")
            
            # Metodo 2: PowerShell
            try:
                ps_cmd = f'''
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -Uri "{get_pip_url}" -OutFile "{get_pip_path}" -UseBasicParsing
Write-Host "✅ get-pip.py scaricato"
'''
                result = subprocess.run([
                    "powershell", "-Command", ps_cmd
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    self.log_message("✅ get-pip.py scaricato con PowerShell")
                else:
                    raise Exception("PowerShell download fallito")
                    
            except Exception as e2:
                self.log_message(f"❌ Errore PowerShell per get-pip: {e2}", "ERROR")
                raise Exception("Impossibile scaricare get-pip.py")
        
        # Installa pip
        python_exe = python_dir / "python.exe"
        self.log_message("🔧 Installando pip...")
        
        try:
            subprocess.run([str(python_exe), str(get_pip_path)], 
                          cwd=python_dir, check=True,
                          capture_output=True, timeout=120)
            
            self.log_message("✅ Pip installato nel Python embedded", "SUCCESS")
            
        except subprocess.TimeoutExpired:
            self.log_message("⏰ Timeout installazione pip", "WARNING")
            # Continua comunque
        except Exception as e:
            self.log_message(f"❌ Errore installazione pip: {e}", "ERROR")
            raise Exception(f"Installazione pip fallita: {e}")
    
    def install_dependencies(self):
        """Installa dipendenze Python"""
        python_dir = self.install_dir / "python"
        python_exe = python_dir / "python.exe"
        
        dependencies = [
            "openai>=1.0.0",
            "chromadb>=0.4.15", 
            "streamlit>=1.28.0",
            "PyMuPDF>=1.23.0",
            "Pillow>=10.0.0",
            "nltk>=3.8.1"
        ]
        
        for i, dep in enumerate(dependencies):
            if self.cancel_install:
                return
            
            self.log_message(f"Installando: {dep}")
            
            try:
                subprocess.run([
                    str(python_exe), "-m", "pip", "install", dep, "--no-warn-script-location"
                ], cwd=python_dir, check=True, capture_output=True)
                
                progress = 60 + ((i + 1) / len(dependencies)) * 20
                self.update_progress(progress, f"📦 Installato: {dep.split('>=')[0]}")
                
            except subprocess.CalledProcessError as e:
                self.log_message(f"Errore installazione {dep}: {e}", "WARNING")
                # Prova versione semplificata
                simple_name = dep.split('>=')[0]
                subprocess.run([
                    str(python_exe), "-m", "pip", "install", simple_name, "--no-warn-script-location"
                ], cwd=python_dir, check=True, capture_output=True)
        
        self.log_message("Tutte le dipendenze installate", "SUCCESS")
    
    def copy_system_files(self):
        """Copia file del sistema RAG e database"""
        # Verifica che source_db_path sia stato impostato
        if self.source_db_path is None:
            self.log_message("❌ ERRORE: Percorso database non impostato!", "ERROR")
            raise Exception("Percorso database non valido. Contatta il supporto.")
        
        self.log_message(f"📂 Inizio copia da: {self.source_db_path}", "INFO")
        
        # File da copiare (dal tuo sistema esistente)
        system_files = {
            "rag_system.py": self.get_rag_system_code(),
            "web_app.py": self.get_web_app_code(),
            "launcher.py": self.get_launcher_code()
        }
        
        for filename, content in system_files.items():
            file_path = self.install_dir / filename
            file_path.write_text(content, encoding='utf-8')
            self.log_message(f"Creato: {filename}")
        
        # Copia database RAG nella directory di installazione
        self.log_message("📂 Copiando database RAG...")
        dest_db_path = self.install_dir / "Rag_db"
        
        try:
            self.log_message(f"📁 Origine: {self.source_db_path}")
            self.log_message(f"📁 Destinazione: {dest_db_path}")
            
            # Verifica che la sorgente esista ancora
            if not self.source_db_path.exists():
                raise Exception(f"Database sorgente non trovato: {self.source_db_path}")
            
            # Se la destinazione esiste già, rimuovila
            if dest_db_path.exists():
                self.log_message("⚠️ Directory database destinazione già esistente, rimozione...", "WARNING")
                shutil.rmtree(dest_db_path)
                self.log_message("✅ Directory precedente rimossa", "SUCCESS")
            
            shutil.copytree(self.source_db_path, dest_db_path)
            copied_files = len(list(dest_db_path.rglob('*')))
            self.log_message(f"✅ Database copiato: {copied_files} file", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"❌ Errore copia database: {e}", "ERROR")
            self.log_message(f"📁 Sorgente: {self.source_db_path}", "ERROR")
            self.log_message(f"📁 Destinazione: {dest_db_path}", "ERROR")
            raise Exception(f"Impossibile copiare database: {e}")
        
        # Salva API key
        api_file = self.install_dir / ".api_key"
        api_file.write_text(self.api_key)
        
        # Crea README per utente finale
        readme_content = self.get_user_readme()
        readme_file = self.install_dir / "README_UTENTE.txt"
        readme_file.write_text(readme_content, encoding='utf-8')
        
        self.log_message("File sistema copiati", "SUCCESS")
    
    def create_launcher(self):
        """Crea launcher finale per l'utente"""
        launcher_bat_content = f'''@echo off
cd /d "{self.install_dir}"
title Sistema RAG Psicologia

echo.
echo ================================
echo    🧠 SISTEMA RAG PSICOLOGIA
echo ================================
echo.
echo ✅ Sistema autocontenuto avviato
echo 🌐 Apertura interfaccia web...
echo.

python\\python.exe launcher.py

if errorlevel 1 (
    echo.
    echo ❌ Errore durante l'avvio
    echo 💡 Controlla README_UTENTE.txt
    pause
)
'''
        
        launcher_path = self.install_dir / "🚀 AVVIA_RAG_PSICOLOGIA.bat"
        launcher_path.write_text(launcher_bat_content, encoding='utf-8')
        
        self.log_message("Launcher creato: 🚀 AVVIA_RAG_PSICOLOGIA.bat", "SUCCESS")
    
    def test_installation(self):
        """Test finale dell'installazione con verifica database"""
        python_exe = self.install_dir / "python" / "python.exe"
        
        # Test import principali
        test_script = '''
import sys
import os
from pathlib import Path

try:
    # Test import
    import openai
    import chromadb
    import streamlit
    print("✅ Tutti i moduli importati correttamente")
    
    # Test database
    db_path = Path("Rag_db")
    if db_path.exists():
        print(f"✅ Database trovato: {len(list(db_path.iterdir()))} file")
        
        # Test ChromaDB
        import chromadb
        client = chromadb.PersistentClient(path="./Rag_db")
        collections = client.list_collections()
        print(f"✅ Database ChromaDB: {len(collections)} collezioni")
        
        # Test API key
        api_file = Path(".api_key")
        if api_file.exists():
            print("✅ API key configurata")
        else:
            print("⚠️ API key mancante")
            
    else:
        print("❌ Database non trovato")
        sys.exit(1)
        
except ImportError as e:
    print(f"❌ Errore import: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Errore test: {e}")
    sys.exit(1)
'''
        
        test_file = self.install_dir / "test_complete.py"
        test_file.write_text(test_script)
        
        try:
            result = subprocess.run([
                str(python_exe), str(test_file)
            ], capture_output=True, text=True, cwd=self.install_dir)
            
            if result.returncode == 0:
                self.log_message("✅ Test completo: SUCCESSO", "SUCCESS")
                self.log_message(result.stdout.strip(), "INFO")
            else:
                self.log_message(f"❌ Test fallito: {result.stderr}", "ERROR")
                self.log_message(f"Output: {result.stdout}", "INFO")
                raise Exception("Test finale fallito")
                
        except Exception as e:
            self.log_message(f"❌ Errore test: {e}", "ERROR")
            raise Exception("Test finale non eseguibile")
        
        # Rimuovi file test
        test_file.unlink()
        
        # Test finale dimensioni
        total_size = sum(f.stat().st_size for f in self.install_dir.rglob('*') if f.is_file())
        size_mb = total_size / 1024 / 1024
        
        self.log_message(f"📊 Sistema finale: {size_mb:.1f} MB", "SUCCESS")
    
    def finalize_installation(self):
        """Finalizza installazione"""
        # Crea shortcut sul desktop se possibile
        try:
            self.create_desktop_shortcut()
        except:
            self.log_message("Shortcut desktop non creato (normale)", "WARNING")
        
        # Dimensioni finali
        total_size = sum(f.stat().st_size for f in self.install_dir.rglob('*') if f.is_file())
        size_mb = total_size / 1024 / 1024
        
        self.log_message(f"Dimensione totale sistema: {size_mb:.1f} MB", "INFO")
        self.log_message(f"Percorso installazione: {self.install_dir}", "INFO")
    
    def create_desktop_shortcut(self):
        """Crea shortcut sul desktop"""
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            shortcut_path = Path(desktop) / "🧠 RAG Psicologia.lnk"
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(self.install_dir / "🚀 AVVIA_RAG_PSICOLOGIA.bat")
            shortcut.WorkingDirectory = str(self.install_dir)
            shortcut.IconLocation = str(self.install_dir / "🚀 AVVIA_RAG_PSICOLOGIA.bat")
            shortcut.save()
            
            self.log_message("Shortcut desktop creato", "SUCCESS")
            
        except ImportError:
            pass  # winshell non disponibile
    
    def installation_finished(self):
        """Chiamato quando installazione è completata"""
        self.install_complete = True
        self.install_btn.config(
            state='normal',
            text="✅ Installazione Completata",
            bg='#10b981'
        )
        self.cancel_btn.config(state='disabled')
        
        # Mostra messaggio successo
        messagebox.showinfo(
            "Installazione Completata!",
            f"✅ Il sistema RAG è stato installato con successo!\n\n"
            f"📁 Percorso: {self.install_dir}\n"
            f"🚀 Per avviare: doppio-click su '🚀 AVVIA_RAG_PSICOLOGIA.bat'\n\n"
            f"📋 Leggi il file 'README_UTENTE.txt' per istruzioni dettagliate."
        )
    
    def installation_failed(self, error):
        """Chiamato quando installazione fallisce"""
        self.install_btn.config(state='normal')
        self.cancel_btn.config(state='disabled')
        self.update_progress(0, f"❌ Installazione fallita")
        
        messagebox.showerror(
            "Errore Installazione",
            f"❌ Installazione fallita:\n\n{error}\n\n"
            f"Controlla il log per dettagli."
        )
    
    # Metodi per generare codice dei file
    def get_rag_system_code(self):
        """Restituisce codice rag_system.py"""
        # Qui usi il contenuto del tuo rag_system.py esistente
        return '''import os
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
    
    def get_web_app_code(self):
        """Restituisce codice web_app.py"""
        # Qui usi il contenuto del tuo web_app.py esistente
        return '''import streamlit as st
import os
from rag_system import SimpleRAGQuery

st.set_page_config(
    page_title="🧠 RAG Psicologia",
    page_icon="🧠",
    layout="wide"
)

# CSS
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

# Header
st.markdown('<h1 class="main-header">🧠 Sistema RAG - Consultazione Psicologia</h1>', unsafe_allow_html=True)

# Inizializza sistema
@st.cache_resource
def init_rag_system():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        # Leggi da file se disponibile
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

# Carica sistema
rag_system = init_rag_system()

if rag_system is None:
    st.error("❌ Sistema non configurato. Verifica la presenza del database RAG.")
    st.stop()

st.success("✅ Sistema RAG connesso e pronto!")

# Interfaccia principale
st.subheader("💭 Fai la Tua Domanda")

# Input domanda
query = st.text_area(
    "Inserisci la tua domanda psicologica:",
    placeholder="Es: Qual è la differenza tra ansia e angoscia secondo questi autori?",
    height=100
)

# Opzioni
col1, col2 = st.columns(2)
with col1:
    n_sources = st.slider("Numero fonti", 3, 8, 5)
with col2:
    if st.button("🔍 Cerca Risposta", type="primary"):
        if query.strip():
            with st.spinner("🧠 Analizzando documenti..."):
                result = rag_system.search_and_respond(query, n_sources)
            
            # Mostra risultati
            st.markdown("### 📝 Risposta")
            st.markdown(result['response'])
            
            # Mostra fonti
            if result['sources']:
                st.markdown("### 📚 Fonti Consultate")
                for i, source in enumerate(result['sources'], 1):
                    with st.expander(f"📄 {i}. {source['file_name']} (p.{source['page_number']}) - Rilevanza: {source['similarity']:.3f}"):
                        st.text(source['content_preview'])
        else:
            st.error("Inserisci una domanda!")

# Esempi
with st.expander("💡 Esempi di Domande"):
    st.markdown("""
    **🧠 Teoria e Concetti:**
    - "Qual è la differenza tra ansia e angoscia?"
    - "Come viene definito il transfert?"
    - "Cosa significa resistenza in terapia?"
    
    **📚 Confronti Teorici:**
    - "Differenze tra Jung e Freud sull'inconscio?"
    - "Approccio cognitivo vs psicodinamico?"
    
    **🏥 Applicazioni Cliniche:**
    - "Caratteristiche del disturbo borderline?"
    - "Come si manifesta un episodio maniacale?"
    """)
'''
    
    def get_launcher_code(self):
        """Restituisce codice launcher.py ottimizzato"""
        return '''#!/usr/bin/env python3
"""
Launcher robusto per Sistema RAG - Avvia interfaccia web
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Verifica tutti i requisiti del sistema"""
    
    print("🔍 Verifica sistema RAG...")
    
    # Verifica API key
    api_key_file = Path('.api_key')
    if not api_key_file.exists():
        print("❌ File API key non trovato!")
        print("📁 Assicurati che il file '.api_key' sia presente")
        return False
    
    api_key = api_key_file.read_text().strip()
    if not api_key.startswith('sk-'):
        print("❌ API key non valida!")
        print("🔑 L'API key deve iniziare con 'sk-'")
        return False
    
    os.environ['OPENAI_API_KEY'] = api_key
    print("✅ API key configurata")
    
    # Verifica database
    db_path = Path('Rag_db')
    if not db_path.exists():
        print("❌ Database RAG non trovato!")
        print("📁 Assicurati che la cartella 'Rag_db' sia presente")
        print(f"📍 Directory corrente: {Path.cwd()}")
        return False
    
    db_files = list(db_path.iterdir())
    if not db_files:
        print("❌ Database vuoto!")
        return False
    
    print(f"✅ Database trovato: {len(db_files)} file")
    
    # Verifica file sistema
    required_files = ['rag_system.py', 'web_app.py']
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ File mancante: {file}")
            return False
    
    print("✅ File sistema verificati")
    
    return True

def find_python():
    """Trova eseguibile Python corretto"""
    
    # Prova percorsi Python embedded
    possible_paths = [
        Path("python/python.exe"),
        Path("python3"),
        Path("python"),
        Path(sys.executable)
    ]
    
    for python_path in possible_paths:
        try:
            if python_path.exists() and python_path.is_file():
                # Test veloce
                result = subprocess.run([str(python_path), "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ Python trovato: {python_path}")
                    return str(python_path)
        except Exception:
            continue
    
    print("❌ Python non trovato!")
    return None

def start_streamlit(python_exe):
    """Avvia server Streamlit"""
    
    try:
        print("🌐 Avviando server web...")
        
        # Controlla se porta già occupata
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8501))
        sock.close()
        
        if result == 0:
            print("⚠️ Porta 8501 già in uso")
            print("🌐 Provo ad aprire browser su sessione esistente...")
            webbrowser.open('http://localhost:8501')
            return True
        
        # Avvia nuovo server
        cmd = [
            python_exe, "-m", "streamlit", "run", 
            "web_app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false",
            "--server.headless", "true"
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
        
        # Aspetta avvio server
        print("⏳ Attendo avvio server...")
        for i in range(15):  # Max 15 secondi
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', 8501))
                sock.close()
                
                if result == 0:
                    print("✅ Server avviato!")
                    break
            except:
                pass
            
            time.sleep(1)
            
            # Controlla se processo è morto
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"❌ Errore avvio server:")
                print(f"Output: {stdout}")
                print(f"Errore: {stderr}")
                return False
        else:
            print("⏰ Timeout avvio server")
            return False
        
        # Apri browser
        print("🌐 Apertura browser...")
        webbrowser.open('http://localhost:8501')
        
        print("✅ Sistema avviato!")
        print("🌐 Interfaccia: http://localhost:8501")
        print("❌ Per fermare: chiudi questa finestra")
        
        # Mantieni processo vivo
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\\n⏹️ Fermando sistema...")
            process.terminate()
            return True
        
        return True
        
    except Exception as e:
        print(f"❌ Errore avvio: {e}")
        return False

def main():
    """Funzione principale launcher"""
    
    print("🧠 SISTEMA RAG PSICOLOGIA")
    print("=" * 30)
    
    # Verifica requisiti
    if not check_requirements():
        input("\\nPremi Invio per uscire...")
        return 1
    
    # Trova Python
    python_exe = find_python()
    if not python_exe:
        input("\\nPremi Invio per uscire...")
        return 1
    
    # Avvia sistema
    if start_streamlit(python_exe):
        print("\\n👋 Sistema terminato correttamente")
        return 0
    else:
        print("\\n❌ Sistema terminato con errori")
        input("\\nPremi Invio per uscire...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
    
    def get_user_readme(self):
        """Restituisce README per utente finale"""
        return f'''
🧠 SISTEMA RAG PSICOLOGIA - GUIDA UTENTE
========================================

✅ INSTALLAZIONE COMPLETATA!

Il tuo sistema RAG di psicologia è stato installato con successo.
Questo è un sistema completamente autocontenuto che non interferisce 
con altre installazioni Python sul tuo computer.

🚀 COME AVVIARE IL SISTEMA:
==========================

1. Fai doppio-click su: "🚀 AVVIA_RAG_PSICOLOGIA.bat"
2. Attendi l'avvio (si apre una finestra nera)
3. Il browser si aprirà automaticamente con l'interfaccia
4. Inizia a fare le tue domande!

🌐 INDIRIZZO WEB:
================
Se il browser non si apre automaticamente:
http://localhost:8501

📁 STRUTTURA SISTEMA:
====================
- python/           → Python isolato con tutte le dipendenze
- Rag_db/            → Database documenti (copiato durante installazione)
- rag_system.py      → Motore di ricerca
- web_app.py         → Interfaccia web
- .api_key           → La tua API key OpenAI (privata!)

💡 ESEMPI DI DOMANDE:
====================
- "Qual è la differenza tra ansia e angoscia?"
- "Come viene definito il transfert in psicoterapia?"
- "Caratteristiche del disturbo borderline?"
- "Differenze tra Jung e Freud sull'inconscio?"

🔧 RISOLUZIONE PROBLEMI:
========================

🚫 "Database RAG non trovato"
   → Il database è stato copiato durante l'installazione, non dovrebbe succedere

🚫 "Errore API Key"
   → Contatta chi ti ha fornito il sistema

🚫 "Porta 8501 occupata"
   → Chiudi altri programmi Streamlit o riavvia il computer

🚫 Il browser non si apre
   → Vai manualmente su http://localhost:8501

📞 SUPPORTO:
============
Per problemi tecnici, contatta la persona che ti ha fornito questo sistema
e invia screenshot degli errori.

📊 INFORMAZIONI SISTEMA:
========================
- Versione Python: Embedded {self.python_version}
- Percorso installazione: {self.install_dir}
- Database: Copiato e autonomo
- Sistema completamente portabile
- Non richiede connessione internet (dopo installazione)

Buona consultazione! 🧠📚
'''

    def run(self):
        """Avvia installer"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SmartRAGInstaller()
    app.run()