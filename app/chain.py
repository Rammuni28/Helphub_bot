
import os
from huggingface_hub import InferenceClient
from langchain.llms.base import LLM
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from pydantic.v1 import BaseModel

# Load environment variable for Hugging Face API
HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

# Initialize embeddings
embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=HUGGINGFACE_API_KEY,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS vectorstore
index = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)



# Set up Hugging Face inference client
client = InferenceClient(
    provider="novita",
    api_key=HUGGINGFACE_API_KEY
)

# Custom LLM class for HuggingFace chat models
class HFChatLLM(LLM, BaseModel):
    model_name: str = "meta-llama/Llama-3.3-70B-Instruct"

    def _call(self, prompt: str, stop=None) -> str:
        messages = [{"role": "user", "content": prompt}]
        stream = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.5,
            max_tokens=2048,
            top_p=0.7,
            stream=True
        )

        response = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta:
                content = chunk.choices[0].delta.content
                if content:
                    response += content
                    print(content, end="", flush=True)

        return response or "No response generated"

    @property
    def _identifying_params(self):
        return {"model_name": self.model_name}

    @property
    def _llm_type(self) -> str:
        return "hf_chat"

# Instantiate LLM and QA chain
hf_llm = HFChatLLM()
qa_chain = RetrievalQA.from_chain_type(
    llm=hf_llm,
    retriever=index.as_retriever(),
    chain_type="stuff"
)
