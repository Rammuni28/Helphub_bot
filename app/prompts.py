# app/prompts.py

from langchain import PromptTemplate

# Prompt used to generate the answer from retrieved docs
QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "You are a helpful support agent for HelpHub. "  
        "Use ONLY the information in CONTEXT to answer the QUESTION. "
        "If the answer isn’t in CONTEXT, reply “I don’t know.”\n\n"
        "CONTEXT:\n{context}\n\n"
        "QUESTION: {question}\n\n"
        "Answer concisely:"
    )
)
