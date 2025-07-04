import streamlit as st
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
    st.error("❌ Sistema non configurato. Riavvia il setup automatico.")
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
