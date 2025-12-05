#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 SECOND BRAIN - Local RAG System for PDFs                                ║
║  Chat with your technical documents - 100% local & private                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
from datetime import datetime


# ══════════════════════════════════════════════════════════════════════════════
# 🎨 NEON COLORS
# ══════════════════════════════════════════════════════════════════════════════

class NeonColors:
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# ══════════════════════════════════════════════════════════════════════════════
# 📄 PDF PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """Extract text from PDF file."""
    try:
        import PyPDF2
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n[PAGE {page_num + 1}]\n{page_text}"
                except Exception as e:
                    print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} Error on page {page_num}: {e}")
            
            return text if text.strip() else None
            
    except ImportError:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} PyPDF2 not installed. Run: pip install PyPDF2")
        return None
    except Exception as e:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Failed to read {pdf_path}: {e}")
        return None


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Characters per chunk
        overlap: Characters to overlap between chunks
        
    Returns:
        List of chunk dictionaries with text and metadata
    """
    chunks = []
    words = text.split()
    
    # Estimate words per chunk (average 5 chars per word)
    words_per_chunk = chunk_size // 5
    overlap_words = overlap // 5
    
    start = 0
    chunk_id = 0
    
    while start < len(words):
        end = min(start + words_per_chunk, len(words))
        chunk_text = ' '.join(words[start:end])
        
        # Extract page number if present
        page_match = chunk_text.find('[PAGE ')
        page_num = "Unknown"
        if page_match != -1:
            try:
                page_end = chunk_text.find(']', page_match)
                page_num = chunk_text[page_match+6:page_end]
            except:
                pass
        
        chunks.append({
            'id': chunk_id,
            'text': chunk_text,
            'page': page_num,
            'start_word': start,
            'end_word': end
        })
        
        chunk_id += 1
        start += words_per_chunk - overlap_words
        
        if start >= len(words):
            break
    
    return chunks


# ══════════════════════════════════════════════════════════════════════════════
# 🧠 EMBEDDINGS (Simple fallback without ML models)
# ══════════════════════════════════════════════════════════════════════════════

def simple_embedding(text: str, dim: int = 384) -> np.ndarray:
    """
    Simple embedding using TF-IDF-like approach (fallback).
    For production, use sentence-transformers or Ollama.
    """
    # Simple hash-based embedding (for demonstration)
    # In production, use: sentence-transformers or Ollama embeddings
    
    words = text.lower().split()
    embedding = np.zeros(dim)
    
    for i, word in enumerate(words[:dim]):
        # Simple hash to vector position
        hash_val = hash(word) % dim
        embedding[hash_val] += 1
    
    # Normalize
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
    
    return embedding


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


# ══════════════════════════════════════════════════════════════════════════════
# 💾 DATABASE
# ══════════════════════════════════════════════════════════════════════════════

class SecondBrainDB:
    """Local vector database for document chunks."""
    
    def __init__(self, db_path: str = "second_brain.json"):
        self.db_path = db_path
        self.documents = []
        self.load()
    
    def load(self):
        """Load database from disk."""
        if Path(self.db_path).exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert embedding lists back to numpy arrays
                    for doc in data:
                        for chunk in doc.get('chunks', []):
                            if 'embedding' in chunk:
                                chunk['embedding'] = np.array(chunk['embedding'])
                    self.documents = data
                    
                print(f"{NeonColors.GREEN}[LOADED]{NeonColors.RESET} Database: {len(self.documents)} documents")
            except Exception as e:
                print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Failed to load database: {e}")
                self.documents = []
    
    def save(self):
        """Save database to disk."""
        try:
            # Convert numpy arrays to lists for JSON serialization
            data = []
            for doc in self.documents:
                doc_copy = doc.copy()
                doc_copy['chunks'] = []
                for chunk in doc.get('chunks', []):
                    chunk_copy = chunk.copy()
                    if 'embedding' in chunk_copy:
                        chunk_copy['embedding'] = chunk_copy['embedding'].tolist()
                    doc_copy['chunks'].append(chunk_copy)
                data.append(doc_copy)
            
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            print(f"{NeonColors.GREEN}[SAVED]{NeonColors.RESET} Database saved")
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Failed to save: {e}")
    
    def add_document(self, filename: str, chunks: List[Dict]):
        """Add document with chunks to database."""
        self.documents.append({
            'filename': filename,
            'indexed_at': datetime.now().isoformat(),
            'num_chunks': len(chunks),
            'chunks': chunks
        })
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict]:
        """Search for most similar chunks."""
        results = []
        
        for doc in self.documents:
            for chunk in doc.get('chunks', []):
                if 'embedding' in chunk:
                    similarity = cosine_similarity(query_embedding, chunk['embedding'])
                    results.append({
                        'filename': doc['filename'],
                        'chunk_id': chunk['id'],
                        'text': chunk['text'],
                        'page': chunk.get('page', 'Unknown'),
                        'similarity': similarity
                    })
        
        # Sort by similarity and return top-k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def stats(self) -> Dict:
        """Get database statistics."""
        total_chunks = sum(doc.get('num_chunks', 0) for doc in self.documents)
        
        return {
            'total_documents': len(self.documents),
            'total_chunks': total_chunks,
            'avg_chunks_per_doc': total_chunks / len(self.documents) if self.documents else 0
        }


# ══════════════════════════════════════════════════════════════════════════════
# 🗂️ INDEXING
# ══════════════════════════════════════════════════════════════════════════════

def index_folder(folder_path: str, db: SecondBrainDB):
    """Index all PDFs in a folder."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Folder not found: {folder_path}")
        return
    
    pdf_files = list(folder.glob("*.pdf"))
    
    if not pdf_files:
        print(f"{NeonColors.YELLOW}[WARN]{NeonColors.RESET} No PDF files found in {folder_path}")
        return
    
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}📚 INDEXING PDFs{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    print(f"{NeonColors.YELLOW}[INFO]{NeonColors.RESET} Found {len(pdf_files)} PDF files\n")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"{NeonColors.CYAN}[{i}/{len(pdf_files)}]{NeonColors.RESET} Processing: {pdf_file.name}")
        
        # Extract text
        text = extract_text_from_pdf(str(pdf_file))
        
        if not text:
            print(f"{NeonColors.RED}[SKIP]{NeonColors.RESET} No text extracted\n")
            continue
        
        # Chunk text
        chunks = chunk_text(text)
        print(f"{NeonColors.GREEN}[CHUNKS]{NeonColors.RESET} Created {len(chunks)} chunks")
        
        # Generate embeddings
        print(f"{NeonColors.YELLOW}[EMBED]{NeonColors.RESET} Generating embeddings...")
        for chunk in chunks:
            chunk['embedding'] = simple_embedding(chunk['text'])
        
        # Add to database
        db.add_document(pdf_file.name, chunks)
        print(f"{NeonColors.GREEN}[DONE]{NeonColors.RESET} Indexed: {pdf_file.name}\n")
    
    # Save database
    db.save()
    
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.GREEN}[SUCCESS]{NeonColors.RESET} Indexing complete!")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


# ══════════════════════════════════════════════════════════════════════════════
# 💬 CHAT INTERFACE
# ══════════════════════════════════════════════════════════════════════════════

def query(question: str, db: SecondBrainDB, top_k: int = 3):
    """Query the knowledge base."""
    print(f"\n{NeonColors.CYAN}{'─' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.YELLOW}[QUERY]{NeonColors.RESET} {question}\n")
    
    # Generate query embedding
    query_embedding = simple_embedding(question)
    
    # Search
    results = db.search(query_embedding, top_k=top_k)
    
    if not results:
        print(f"{NeonColors.RED}[NO RESULTS]{NeonColors.RESET} No relevant documents found\n")
        return
    
    # Display results
    print(f"{NeonColors.GREEN}[FOUND]{NeonColors.RESET} Top {len(results)} relevant chunks:\n")
    
    for i, result in enumerate(results, 1):
        print(f"{NeonColors.MAGENTA}[{i}]{NeonColors.RESET} {NeonColors.BOLD}{result['filename']}{NeonColors.RESET} (Page {result['page']})")
        print(f"{NeonColors.CYAN}Similarity:{NeonColors.RESET} {result['similarity']:.2%}")
        print(f"{NeonColors.GREEN}Content:{NeonColors.RESET} {result['text'][:200]}...")
        print()


def interactive_chat(db: SecondBrainDB):
    """Interactive chat mode."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}💬 INTERACTIVE CHAT MODE{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    print(f"{NeonColors.YELLOW}[INFO]{NeonColors.RESET} Type your questions. Type 'exit' to quit.\n")
    
    while True:
        try:
            question = input(f"{NeonColors.GREEN}You:{NeonColors.RESET} ")
            
            if question.lower() in ['exit', 'quit', 'q']:
                print(f"\n{NeonColors.YELLOW}[EXIT]{NeonColors.RESET} Goodbye!\n")
                break
            
            if not question.strip():
                continue
            
            query(question, db, top_k=3)
            
        except KeyboardInterrupt:
            print(f"\n\n{NeonColors.YELLOW}[EXIT]{NeonColors.RESET} Chat terminated\n")
            break
        except Exception as e:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} {e}")


# ══════════════════════════════════════════════════════════════════════════════
# 📊 STATS
# ══════════════════════════════════════════════════════════════════════════════

def show_stats(db: SecondBrainDB):
    """Display database statistics."""
    stats = db.stats()
    
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}📊 DATABASE STATISTICS{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    print(f"{NeonColors.YELLOW}Total Documents:{NeonColors.RESET} {stats['total_documents']}")
    print(f"{NeonColors.YELLOW}Total Chunks:{NeonColors.RESET} {stats['total_chunks']}")
    print(f"{NeonColors.YELLOW}Avg Chunks/Doc:{NeonColors.RESET} {stats['avg_chunks_per_doc']:.1f}")
    
    print(f"\n{NeonColors.GREEN}Documents indexed:{NeonColors.RESET}")
    for i, doc in enumerate(db.documents, 1):
        print(f"  {NeonColors.CYAN}{i}.{NeonColors.RESET} {doc['filename']} ({doc['num_chunks']} chunks)")
    
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


# ══════════════════════════════════════════════════════════════════════════════
# 🚀 MAIN CLI
# ══════════════════════════════════════════════════════════════════════════════

def print_help():
    """Print usage help."""
    print(f"\n{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}")
    print(f"{NeonColors.BOLD}{NeonColors.MAGENTA}📚 SECOND BRAIN - Usage{NeonColors.RESET}")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")
    
    print(f"{NeonColors.GREEN}Commands:{NeonColors.RESET}\n")
    print(f"  {NeonColors.YELLOW}index <folder>{NeonColors.RESET}     Index all PDFs in folder")
    print(f"  {NeonColors.YELLOW}query <question>{NeonColors.RESET}   Search for answer")
    print(f"  {NeonColors.YELLOW}chat{NeonColors.RESET}               Interactive chat mode")
    print(f"  {NeonColors.YELLOW}stats{NeonColors.RESET}              Show database statistics")
    print(f"  {NeonColors.YELLOW}help{NeonColors.RESET}               Show this help")
    
    print(f"\n{NeonColors.GREEN}Examples:{NeonColors.RESET}\n")
    print(f"  {NeonColors.CYAN}python second_brain.py index ./documents{NeonColors.RESET}")
    print(f"  {NeonColors.CYAN}python second_brain.py query \"What is microservices?\"{NeonColors.RESET}")
    print(f"  {NeonColors.CYAN}python second_brain.py chat{NeonColors.RESET}")
    print(f"  {NeonColors.CYAN}python second_brain.py stats{NeonColors.RESET}")
    
    print(f"\n{NeonColors.YELLOW}[NOTE]{NeonColors.RESET} This uses simple embeddings for demonstration.")
    print(f"{NeonColors.YELLOW}[NOTE]{NeonColors.RESET} For production, install: pip install sentence-transformers")
    print(f"{NeonColors.CYAN}{'═' * 78}{NeonColors.RESET}\n")


def main():
    """Main CLI entry point."""
    db = SecondBrainDB()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "index":
        if len(sys.argv) < 3:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Usage: index <folder>")
            return
        
        folder_path = sys.argv[2]
        index_folder(folder_path, db)
    
    elif command == "query":
        if len(sys.argv) < 3:
            print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Usage: query <question>")
            return
        
        question = ' '.join(sys.argv[2:])
        query(question, db)
    
    elif command == "chat":
        interactive_chat(db)
    
    elif command == "stats":
        show_stats(db)
    
    elif command == "help":
        print_help()
    
    else:
        print(f"{NeonColors.RED}[ERROR]{NeonColors.RESET} Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{NeonColors.YELLOW}[EXIT]{NeonColors.RESET} Terminated\n")
    except Exception as e:
        print(f"\n{NeonColors.RED}[FATAL]{NeonColors.RESET} {e}\n")

