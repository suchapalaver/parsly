FROM python:3.9-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

FROM python:3.9-slim

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app

COPY . /app

ENV PATH="/opt/venv/bin:$PATH"

ENV OPENAI_API_KEY_FILE=.env

EXPOSE 80

CMD ["python", "parsey.py"]
