# 🧠 HelpHub-Bot

An AI chatbot for the fictional SaaS product **HelpHub**, powered by Hugging Face's LLMs and semantic search using FAISS. Provides context-aware answers based on Markdown documentation.

---

## 🚀 Features

- ⚡️ FAISS-powered instant search over Markdown knowledge base
- 💬 Context-aware conversations with HuggingFace LLM integration
- 🧠 Conversation memory for natural interactions
- ❓ Graceful fallback for unanswerable questions
- 📊 SQLite logging of Q&A sessions and user feedback (👍/👎)
- 🖥️ Modern web interface with SocketIO real-time communication

---

## 🏗️ Project Structure

    helphub-bot/
    ├── app/
    │   ├── app.py          # Flask server & WebSocket handler
    │   ├── chain.py        # FAISS/LLM integration logic
    │   ├── indexer.py      # Markdown indexing system
    │   ├── prompts.py      # Response generation templates
    │   └── templates/
    │       └── chat.html   # Chat interface
    ├── kb/                 # Knowledge base (Markdown files)
    ├── faiss_index/        # Auto-generated vector store
    ├── analytics/          # Feedback database (SQLite)
    ├── Dockerfile          # Container configuration
    ├── requirements.txt    # Python dependencies
    └── README.md           # Project documentation

---
🧪 Quick Start (Docker)

# Build the Docker image
    docker build -t helphub-bot .

# Run the container (replace <HF_TOKEN> with your HuggingFace API key)
    docker run -p 5000:5000 -e HUGGINGFACEHUB_API_TOKEN=<HF_TOKEN> helphub-bot

Access the chat interface at 👉 http://localhost:5000

🔧 Development Setup

Clone repository:


     git clone https://github.com/Rammuni28/Helphub_bot
     cd Helphub_bot

Create virtual environment:



    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:



    pip install -r requirements.txt

 Set environment variables:



    export HUGGINGFACEHUB_API_TOKEN=<your-hf-token-here>

Build search index:



    python app/indexer.py

Start development server:


    python -m app.app


📖 Documentation
	•	Inline docs: All modules (app/app.py, app/chain.py, app/indexer.py) include doc-strings and comments to explain key logic.
	•	Knowledge Base: Browse kb/*.md for product concept, features, pricing, use cases, FAQs, troubleshooting, security, analytics, and developer guides.
	•	API Endpoints:
	•	GET / → Chat UI
	•	WebSocket user_message → ask question
	•	WebSocket user_rating → submit rating
	•	GET /analytics → JSON summary of total questions, satisfaction scores, and question-type breakdown.


📊 Analytics

    Feedback gets stored in analytics/feedback.db

    Visit /analytics to view basic stats in JSON

📄 License

This project is for demo and educational purposes. Feel free to adapt and extend it!

