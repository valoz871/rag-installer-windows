# 🧠 Sistema RAG Psicologia - Installer Windows

**Sistema di consultazione intelligente per documenti di psicologia con installer automatico per Windows.**

## 🚀 Caratteristiche

- ✅ **Installer EXE automatico** - Zero configurazione manuale
- ✅ **Installa Python automaticamente** - Non richiede Python preinstallato  
- ✅ **Sistema RAG completo** - ChromaDB + OpenAI + Streamlit
- ✅ **Interface web intuitiva** - Facile da usare per non programmatori
- ✅ **Database vettoriale** - Ricerca semantica avanzata
- ✅ **Completamente portatile** - Sistema autocontenuto

## 📦 Download

### Per Utenti Finali (Windows):
1. Vai alla sezione **[Releases](../../releases)**
2. Scarica l'ultima versione: `RAG_Psicologia_Installer.exe`
3. Scarica o assicurati di avere la cartella `Rag_db` con il database

### Per Sviluppatori:
```bash
git clone https://github.com/tuouser/rag-psicologia.git
cd rag-psicologia
```

## 🔧 Uso dell'Installer (Utenti Finali)

### 1. Preparazione
- ✅ Windows 10/11 (64-bit)
- ✅ Connessione internet
- ✅ OpenAI API Key (inizia con `sk-`)
- ✅ Database RAG (cartella `Rag_db`)

### 2. Installazione
1. **Esegui** `RAG_Psicologia_Installer.exe`
2. **Seleziona** directory di installazione (o lascia default)
3. **Scegli** la cartella `Rag_db` (usa Auto-Rileva o Sfoglia)
4. **Inserisci** la tua OpenAI API Key
5. **Click** "Installa Sistema Completo"
6. **Attendi** 5-10 minuti per l'installazione automatica

### 3. Utilizzo
- **Avvio**: Doppio-click sul collegamento desktop "Sistema RAG Psicologia"
- **Interface**: Si apre automaticamente nel browser su `http://localhost:8501`
- **Domande**: Inserisci domande di psicologia e ottieni risposte con fonti

## 💻 Sviluppo

### Build EXE Locale
```bash
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "RAG_Psicologia_Installer" complete_windows_installer.py
```

### Build Automatica (GitHub Actions)
- **Push** su branch `main` triggera la build automatica
- **Download** l'EXE da **Actions** → **Artifacts**
- **Release** automatica per ogni build

### Struttura Progetto
```
├── complete_windows_installer.py   # Installer principale
├── .github/workflows/build-installer.yml   # GitHub Actions
├── requirements.txt                # Dipendenze build
├── README.md                      # Questo file
└── brain.ico                     # Icona (opzionale)
```

## 🧠 Funzionalità Sistema RAG

### Interfaccia Web
- **Campo domanda** con esempi di prompt
- **Slider fonti** per controllare numero documenti consultati
- **Risultati strutturati** con risposte e fonti citate
- **Preview fonti** con rilevanza e contenuto

### Esempi di Domande
- *"Qual è la differenza tra ansia e angoscia?"*
- *"Come viene definito il transfert?"*
- *"Caratteristiche del disturbo borderline?"*
- *"Differenze tra Jung e Freud sull'inconscio?"*

### Tecnologie
- **ChromaDB** - Database vettoriale per ricerca semantica
- **OpenAI** - Embeddings e generazione risposte (GPT-4)
- **Streamlit** - Interfaccia web moderna e intuitiva
- **Python** - Backend e orchestrazione

## ⚙️ Configurazione

### OpenAI API Key
- Richiesta durante installazione
- Salvata localmente in `.api_key`
- Utilizzata per embeddings e generazione risposte

### Database RAG
- Formato: ChromaDB con embedding precalcolati
- Contenuto: Documenti di psicologia processati
- Dimensione tipica: 100-500MB

## 🛠️ Risoluzione Problemi

### Installer
- **"Python non installabile"**: Esegui come amministratore
- **"Database non trovato"**: Verifica percorso cartella Rag_db
- **"API Key non valida"**: Controlla che inizi con "sk-"

### Sistema RAG  
- **"ChromaDB error"**: Reinstalla Visual C++ Redistributable
- **"OpenAI timeout"**: Verifica connessione e quota API
- **"Port 8501 busy"**: Chiudi altre istanze Streamlit

### Log e Debug
- Log installazione visibile nell'installer
- Log sistema in console launcher
- File di log salvati nella directory di installazione

## 📞 Supporto

### Per Utenti
- Controlla prima la sezione **Risoluzione Problemi**
- Includi screenshot degli errori
- Specifica versione Windows

### Per Sviluppatori
- Apri **Issue** su GitHub
- Includi log completi e passi per riprodurre
- Testa prima con build locale

## 📄 Licenza

Progetto privato per uso specifico in ambito psicologico.

## 🔄 Versioni

### v1.0.x
- ✅ Installer automatico Windows
- ✅ Sistema RAG completo  
- ✅ Interface Streamlit
- ✅ Build GitHub Actions

---

**Creato per rendere la consultazione di documenti psicologici semplice e accessibile a tutti.** 🧠✨