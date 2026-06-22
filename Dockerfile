FROM python:3.11-slim

WORKDIR /app

# Dépendances système minimales (certs SSL pour httpx)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Utilisateur non-root pour la sécurité
RUN useradd -m yokubo
USER yokubo

CMD ["python", "main.py"]
