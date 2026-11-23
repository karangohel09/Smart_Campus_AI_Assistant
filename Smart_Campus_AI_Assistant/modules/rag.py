from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
def extract_pdf_text(file):
    reader=PdfReader(file)
    return "\\n".join(page.extract_text() or "" for page in reader.pages)
def retrieve_context(text,question,top_k=3):
    clean=re.sub(r"\\s+"," ",text).strip()
    chunks=[clean[i:i+900] for i in range(0,len(clean),750)]
    if not chunks: return ""
    if len(chunks)==1: return chunks[0]
    v=TfidfVectorizer(stop_words="english")
    matrix=v.fit_transform(chunks+[question])
    scores=cosine_similarity(matrix[-1],matrix[:-1]).flatten()
    best=scores.argsort()[-min(top_k,len(chunks)):][::-1]
    return "\\n\\n--- Retrieved passage ---\\n\\n".join(chunks[i] for i in best)
