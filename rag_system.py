import os
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
            context = "\n\n".join([
                f"[FONTE] {Path(r['metadata']['source_file']).name}, pagina {r['metadata']['page_number']}:\n{r['content']}"
                for r in top_results
            ])
            
            gpt_response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sei un esperto di psicologia. Rispondi basandoti sui documenti forniti. Cita sempre le fonti nel formato [Fonte: nome_file.pdf, pagina X]."},
                    {"role": "user", "content": f"DOMANDA: {query}\n\nDOCUMENTI:\n{context}"}
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
