# use a lightweight python image
FROM python:3.11-slim

# set the working directory in the container
WORKDIR /app

# install system dependencies for FAISS and PDF processing
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# copy the requirements file into the container and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the source code into the container
COPY . .

# expose ports for the FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501