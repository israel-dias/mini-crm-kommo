FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# deps do sistema (psycopg / build básico)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml* requirements.txt* /app/

# Instala dependências (se você usa requirements.txt, ele pega; se usa pyproject, também funciona)
RUN pip install --upgrade pip \
    && if [ -f requirements.txt ]; then pip install -r requirements.txt; fi \
    && if [ -f pyproject.toml ]; then pip install -e .; fi

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
