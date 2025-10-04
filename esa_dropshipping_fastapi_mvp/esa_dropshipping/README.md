# ESA Dropshipping – Backend FastAPI (MVP)

Núcleo de backend para tu programa de dropshipping híbrido con Deliver Fever.

## Ejecutar localmente
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Variables de entorno
- `DATABASE_URL` — SQLite local o PostgreSQL en producción.
- `DF_*` — Dirección de tu cuenta Deliver Fever.
