from fastapi import FastAPI, Query
from pathlib import Path
import yaml
import os

app = FastAPI(
    title="Pipeline as Art API",
    description="A living, bilingual pipeline that documents itself.",
    version="0.1.0",
)

I18N_DIR = Path(__file__).parent / "i18n"

def t(lang: str, key: str) -> str:
    file = I18N_DIR / f"{lang}.yaml"
    if not file.exists():
        file = I18N_DIR / "en.yaml"
    data = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
    node = data
    for part in key.split("."):
        node = node.get(part, {})
    return node if isinstance(node, str) else key

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/")
def root(lang: str = Query(default="en", pattern="^(en|es|de)$")):
    return {"message": t(lang, "root.greeting")}

@app.get("/about")
def about(lang: str = Query(default="en", pattern="^(en|es|de)$")):
    return {
        "title": t(lang, "about.title"),
        "mission": t(lang, "about.mission"),
        "stack": ["FastAPI", "Caddy", "Postgres", "Redis"],
        "env": {
            "database_url_set": bool(os.getenv("DATABASE_URL")),
            "redis_url_set": bool(os.getenv("REDIS_URL")),
        },
    }
