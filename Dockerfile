# app/Dockerfile

FROM python:3.11-slim

WORKDIR /syncwebapp

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ekemainaiML/syncwebapp.git .


COPY . .
RUN pip install --no-cache-dir --upgrade -r /syncwebapp/requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]