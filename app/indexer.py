import os
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

docs = []
kb_path = "kb"

# Loop through all markdown files in the 'kb/' folder
for file_name in os.listdir(kb_path):
    if file_name.endswith(".md"):
        file_path = os.path.join(kb_path, file_name)
        loader = TextLoader(file_path)
        docs.extend(loader.load())

# Split documents
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(docs)

# Load embeddings using HuggingFace API
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=os.environ["HUGGINGFACEHUB_API_TOKEN"],  
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Store in FAISS
db = FAISS.from_documents(documents, embeddings)
db.save_local("faiss_index")
print("✅ Knowledge base indexed successfully!")
