# Troubleshooting Common Issues

**Chatbot Not Responding**  
- Ensure your FAISS index is built (`kb/` → `indexer.py`)  
- Check your HF token is set: `export HUGGINGFACEHUB_API_TOKEN=…`

**Slack Messages Not Delivered**  
- Verify the Slack app has posting permissions  
- Check your channel IDs in Integrations settings  

**500‑Errors in Flask**  
- Run `python -m app.app` from the project root  
- Confirm `templates/chat.html` lives under `app/templates/`
