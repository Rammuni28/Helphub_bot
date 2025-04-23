# Use Python slim base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy all files into the image
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directories if not already present (for safety)
RUN mkdir -p analytics faiss_index

# Build the FAISS vector index before launching app
RUN python app/indexer.py

# Expose Flask app port
EXPOSE 5000

# Run the application
CMD ["python", "-m", "app.app"]
