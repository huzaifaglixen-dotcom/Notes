
# main.py
"""
Production-style educational RAG example.
Features:
- Read PDF
- Recursive chunking
- SentenceTransformer embeddings
- ChromaDB Persistent
- Metadata (source/page)
- MD5 hash
- hash.json auto create/update
- Auto re-index when PDF changes
- Gemini answer generation
"""

import os, json, hashlib
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai

PDF_PATH = "sample.pdf"
DB_PATH = "./my_chroma_db"
COLLECTION_NAME = "pdf_chunks_collection"
HASH_FILE = "hash.json"
GEMINI_API_KEY = "Your_Google_API_Key_Here"

model = SentenceTransformer("all-MiniLM-L6-v2")
gemini = genai.Client(api_key=GEMINI_API_KEY)
db = chromadb.PersistentClient(path=DB_PATH)
collection = db.get_or_create_collection(COLLECTION_NAME)

def calculate_pdf_hash(path):
    with open(path,"rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def load_hashes():
    if not os.path.exists(HASH_FILE):
        with open(HASH_FILE,"w") as f:
            json.dump({},f,indent=4)
    with open(HASH_FILE,"r") as f:
        return json.load(f)

def save_hashes(h):
    with open(HASH_FILE,"w") as f:
        json.dump(h,f,indent=4)

def read_pdf(path):
    reader=PdfReader(path)
    pages=[]
    for i,p in enumerate(reader.pages, start=1):
        t=p.extract_text() or ""
        pages.append((i,t))
    return pages

def create_chunks(pages):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n","\n"," ",""]
    )
    docs=[]; ids=[]; metas=[]; embs=[]
    c=0
    for page_no,text in pages:
        for chunk in splitter.split_text(text):
            docs.append(chunk)
            ids.append(f"{os.path.basename(PDF_PATH)}_chunk_{c}")
            metas.append({"source":PDF_PATH,"page":page_no})
            embs.append(model.encode(chunk).tolist())
            c+=1
    return ids,docs,embs,metas

def index_pdf():
    ids,docs,embs,metas=create_chunks(read_pdf(PDF_PATH))
    collection.add(ids=ids,documents=docs,embeddings=embs,metadatas=metas)

def delete_pdf_chunks():
    collection.delete(where={"source":PDF_PATH})

def sync_pdf():
    hashes=load_hashes()
    current=calculate_pdf_hash(PDF_PATH)
    if PDF_PATH not in hashes:
        print("New PDF -> indexing")
        index_pdf()
    elif hashes[PDF_PATH]!=current:
        print("PDF changed -> reindex")
        delete_pdf_chunks()
        index_pdf()
    else:
        print("PDF unchanged -> skip indexing")
        return
    hashes[PDF_PATH]=current
    save_hashes(hashes)

def ask(query):
    qemb=model.encode(query).tolist()
    res=collection.query(query_embeddings=[qemb],n_results=3)
    context="\n\n".join(res["documents"][0])
    prompt=f"""Answer ONLY from context.
If answer not found reply:
'I couldn't find that information in the PDF.'

Context:
{context}

Question:
{query}
"""
    ans=gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print("\nAnswer:\n")
    print(ans.text)
    print("\nSources:")
    for m,d in zip(res["metadatas"][0],res["distances"][0]):
        print(f"Page {m['page']} | {m['source']} | Distance={d}")

def main():
    sync_pdf()
    while True:
        q=input("\nAsk (exit to quit): ")
        if q.lower()=="exit":
            break
        ask(q)

if __name__=="__main__":
    main()



