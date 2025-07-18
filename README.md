# 🧠 SISTEMA RAG PSICOLOGIA - GUIDA COMPLETA v2.0

## ⚠️ PRIMA DI INIZIARE - IMPORTANTE!

### 📦 Cosa Ti Serve:
1. **✅ RAG_Psicologia_Installer.exe** (l'installer scaricato)
2. **✅ Cartella "Rag_db"** (contiene il database dei documenti)
3. **✅ OpenAI API Key** (inizia con "sk-" - fornita dal creatore)

> **💡 NOVITÀ v2.0:** L'installer ora può trovare automaticamente il database anche se è in cartelle diverse!

---

## 🚀 INSTALLAZIONE GUIDATA (SEMPLICE)

### Passo 1: Preparazione
- Assicurati di avere entrambi i file (installer + cartella Rag_db)
- **NON** è necessario che siano nella stessa cartella
- Hai bisogno di ~500MB di spazio libero

### Passo 2: Avvio Installer
1. **Doppio-click** su `RAG_Psicologia_Installer.exe`
2. Se Windows chiede conferma, click **"Sì"** o **"Esegui comunque"**
3. Si aprirà l'interfaccia dell'installer

### Passo 3: Configurazione Smart
**📁 Directory Installazione:**
- Lascia il percorso predefinito OPPURE
- Click 📂 per scegliere dove installare

**🗄️ Database Rag_db:**
- Click **"🔍 Auto-rileva"** per trovare automaticamente il database
- OPPURE click 📂 per selezionarlo manualmente
- Click **"✅ Testa Database"** per verificare che sia valido

**🔑 API Key OpenAI:**
- Inserisci la chiave fornita (inizia con "sk-")
- Verrà nascosta con asterischi per sicurezza

### Passo 4: Installazione
1. Click **"🚀 Installa Sistema"**
2. **Attendi 5-10 minuti** (download automatico Python + pacchetti)
3. Segui la barra di progresso
4. ✅ **Installazione completata!**

### Passo 5: Primo Avvio
- Il browser si aprirà automaticamente
- Se non si apre: doppio-click su `🚀 AVVIA_RAG_PSICOLOGIA.bat`
- Interfaccia disponibile su: http://localhost:8501

---

## 🔍 NUOVE FUNZIONALITÀ v2.0

### 🎯 Auto-Detection Intelligente
- **Trova automaticamente** la cartella Rag_db ovunque sia
- Cerca in cartelle comuni: Desktop, Download, directory progetto
- **Validazione automatica** del database

### 🛡️ Installazione Robusta
- **Gestione errori completa** con retry automatico
- **Progress bar dettagliata** per ogni fase
- **Possibilità di annullare** durante l'installazione
- **Test automatici** di tutti i componenti

### 🧪 Test e Validazione
- **Verifica automatica** di Python, pacchetti e database
- **Test di integrazione** completo del sistema
- **Messaggi di errore chiari** con soluzioni suggerite

---

## 💭 COME USARE IL SISTEMA

### Esempi di Domande Efficaci:

**🧠 Concetti Teorici:**
```
"Qual è la differenza tra ansia e angoscia secondo Freud?"
"Come viene definito il transfert in psicoanalisi?"
"Caratteristiche del Super-Io nella teoria freudiana?"
```

**📊 Disturbi e Diagnosi:**
```
"Criteri diagnostici del disturbo borderline di personalità?"
"Come si manifesta un episodio maniacale?"
"Sintomi della depressione maggiore secondo il DSM-5?"
```

**🔄 Confronti Teorici:**
```
"Differenze tra Jung e Freud sull'inconscio?"
"Approccio cognitivo vs psicodinamico alla depressione?"
"Terapia sistemica vs terapia individuale?"
```

**🏥 Applicazioni Cliniche:**
```
"Tecniche di intervento per disturbi d'ansia?"
"Come condurre un primo colloquio clinico?"
"Strategie terapeutiche per adolescenti?"
```

### 🎛️ Opzioni Avanzate:
- **Slider "Numero fonti"**: Più fonti = risposte più complete
- **Visualizzazione fonti**: Vedi da quali documenti proviene ogni informazione
- **Percentuale rilevanza**: Quanto ogni fonte è pertinente alla domanda

---

## 🔧 RISOLUZIONE PROBLEMI

### ❌ Errori Durante Installazione

**"Auto-rileva non trova il database"**
```
✅ Soluzioni:
• Usa il pulsante 📂 per selezionare manualmente la cartella Rag_db
• Assicurati che la cartella contenga file (non sia vuota)
• Prova a copiare Rag_db sul Desktop e riprova auto-rileva
```

**"Errore download Python"**
```
✅ Soluzioni:
• Verifica connessione internet
• Riprova l'installazione (l'installer riproverà automaticamente)
• Disabilita temporaneamente antivirus
```

**"Installazione pacchetti fallita"**
```
✅ Soluzioni:
• L'installer riprova automaticamente
• Se persiste, verifica firewall/proxy aziendale
• Prova da una rete diversa
```

**"Database non valido"**
```
✅ Soluzioni:
• Usa "✅ Testa Database" per verificare
• Assicurati di aver selezionato la cartella Rag_db corretta
• Contatta chi ti ha fornito il sistema se il database è corrotto
```

### ❌ Errori Durante l'Uso

**"Sistema RAG non configurato"**
```
✅ Soluzioni:
• Riavvia tramite 🚀 AVVIA_RAG_PSICOLOGIA.bat
• Verifica che file .api_key sia presente
• Reinstalla se il problema persiste
```

**"Porta 8501 occupata"**
```
✅ Soluzioni:
• Chiudi altre applicazioni Streamlit
• Riavvia il computer
• Usa Task Manager per chiudere processi python.exe
```

**"Errore OpenAI API"**
```
✅ Soluzioni:
• Verifica che l'API Key sia corretta
• Controlla credito disponibile sul tuo account OpenAI
• Contatta il supporto se l'API Key non funziona
```

**"Risposte poco rilevanti"**
```
✅ Soluzioni:
• Riformula la domanda con termini più specifici
• Aumenta il numero di fonti consultate (slider)
• Usa terminologia tecnica presente nei documenti
• Specifica autore o approccio teorico
```

---

## 🏃‍♂️ AVVIO RAPIDO FUTURO

Dopo la prima installazione:

1. **Doppio-click** su `🚀 AVVIA_RAG_PSICOLOGIA.bat`
2. **Attendi** apertura automatica browser
3. **Inizia** a fare domande!

> **🌐 Indirizzo locale:** http://localhost:8501  
> **❌ Per chiudere:** Chiudi la finestra nera che si apre con il launcher

---

## 📊 CARATTERISTICHE TECNICHE

### 🛡️ Sicurezza e Privacy
- ✅ **Completamente offline** dopo installazione
- ✅ **Database locale**, nessun dato inviato esternamente
- ✅ **API Key sicura**, memorizzata localmente
- ✅ **Nessuna telemetria** o raccolta dati

### ⚡ Performance
- 🧠 **Motore AI**: OpenAI GPT-4 + Embeddings semantici
- 🗃️ **Database**: ChromaDB vettoriale locale
- ⚡ **Ricerca**: Risultati in millisecondi
- 💾 **Dimensione**: ~200-300MB totali

### 🔧 Sistema
- 🐍 **Python**: 3.11.8 embedded (isolato)
- 🌐 **Interfaccia**: Streamlit web app
- 🖥️ **Compatibilità**: Windows 10/11 (64-bit)
- 📦 **Portabilità**: Sistema completamente autocontenuto

---

## 💡 CONSIGLI PER L'USO OTTIMALE

### ✅ Domande che Funzionano Bene:
- **Specifiche**: "Criteri DSM-5 per il disturbo bipolare"
- **Comparative**: "Differenze tra Freud e Jung sull'Es"
- **Tecniche**: "Come applicare la terapia cognitiva all'ansia"
- **Con autore**: "Definizione di transfert secondo Lacan"

### ❌ Domande Meno Efficaci:
- **Troppo generiche**: "Dimmi tutto sulla psicologia"
- **Senza contesto**: "Cos'è la depressione"
- **Non presenti**: Argomenti non coperti dal database

### 🎯 Massimizza l'Efficacia:
1. **Usa termini tecnici** presenti nei documenti
2. **Specifica l'approccio** teorico di interesse
3. **Consulta sempre le fonti** mostrate per approfondire
4. **Riprova con riformulazioni** se non soddisfatto
5. **Aumenta le fonti** per argomenti complessi

---

## 📞 SUPPORTO

### 🆘 Serve Aiuto?
Per problemi tecnici, contatta chi ti ha fornito il sistema con:

📧 **Informazioni da includere:**
- Screenshot dell'errore
- Descrizione di cosa stavi facendo
- Sistema operativo (Windows 10/11)
- Se l'errore è durante installazione o uso

🔧 **File di log utili:**
- Messaggi nella finestra nera del launcher
- Eventuali file di errore generati

---

## 🎓 CONCLUSIONE

Il **Sistema RAG Psicologia v2.0** ti permette di:

✅ **Consultare rapidamente** migliaia di documenti di psicologia  
✅ **Ottenere risposte precise** con citazioni delle fonti  
✅ **Esplorare connessioni** tra diversi autori e approcci  
✅ **Lavorare offline** in totale privacy  

**Buona esplorazione del mondo della psicologia! 🧠📚✨**

---

*Sistema RAG Psicologia v2.0 | Installer Robusto*  
*Aggiornato: Dicembre 2024*