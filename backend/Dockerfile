FROM python:3.13-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8081
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 8081
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8081/healthz')"
CMD exec python transformsql_engine.py --serve --port ${PORT}
