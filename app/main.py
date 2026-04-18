"""FastAPI web app for the P95.AI lead scoring and outreach workflow."""

from __future__ import annotations

import base64
import io
import os
from typing import Any, Dict, List

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from mock_leads import generate_leads
from models.scorer import get_top_leads, score_dataframe
from outreach.generator import generate_outreach_batch
from score_leads import validate_columns


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

app = FastAPI(
    title="P95.AI Lead Pipeline",
    description="Web app and API for lead scoring and outreach generation.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def _dataframe_to_csv_base64(df: pd.DataFrame) -> str:
    csv_text = df.to_csv(index=False)
    return base64.b64encode(csv_text.encode("utf-8")).decode("utf-8")


def _preview_rows(df: pd.DataFrame, limit: int = 10) -> List[Dict[str, Any]]:
    preview_df = df.head(limit).fillna("")
    return preview_df.to_dict(orient="records")


def _load_csv_from_upload(upload: UploadFile) -> pd.DataFrame:
    if not upload.filename or not upload.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    raw = upload.file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")

    try:
        return pd.read_csv(io.BytesIO(raw))
    except Exception as exc:  # pragma: no cover - defensive parsing
        raise HTTPException(status_code=400, detail=f"Unable to parse CSV: {exc}") from exc


def _tier_counts(df: pd.DataFrame) -> Dict[str, int]:
    counts = df["tier"].value_counts().to_dict() if "tier" in df.columns else {}
    return {tier: int(counts.get(tier, 0)) for tier in ["Hot", "Warm", "Cold"]}


def _score_summary(df: pd.DataFrame) -> Dict[str, Any]:
    return {
        "total_leads": int(len(df)),
        "average_score": round(float(df["raw_score"].mean()), 1) if not df.empty else 0.0,
        "max_score": int(df["raw_score"].max()) if not df.empty else 0,
        "min_score": int(df["raw_score"].min()) if not df.empty else 0,
        "tier_counts": _tier_counts(df),
        "top_leads": _preview_rows(get_top_leads(df, n=min(10, len(df))), limit=10) if not df.empty else [],
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Render the main dashboard."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "has_anthropic_key": bool(os.getenv("ANTHROPIC_API_KEY")),
        },
    )


@app.get("/api/health")
async def health() -> Dict[str, Any]:
    """Simple health endpoint for deployments."""
    return {
        "status": "ok",
        "service": "p95-lead-pipeline",
        "anthropic_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
    }


@app.post("/api/mock-leads")
async def api_mock_leads(count: int = Form(220)) -> Dict[str, Any]:
    """Generate mock leads and return CSV + preview."""
    if count < 1 or count > 5000:
        raise HTTPException(status_code=400, detail="Count must be between 1 and 5000.")

    df = generate_leads(count)
    return {
        "filename": f"mock_leads_{count}.csv",
        "row_count": int(len(df)),
        "columns": list(df.columns),
        "preview_rows": _preview_rows(df),
        "csv_base64": _dataframe_to_csv_base64(df),
    }


@app.post("/api/score")
async def api_score_leads(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Score a Clay-export CSV and return results."""
    df = _load_csv_from_upload(file)

    try:
        validate_columns(df)
    except SystemExit as exc:
        raise HTTPException(status_code=400, detail="CSV is missing one or more required columns.") from exc

    scored_df = score_dataframe(df).sort_values("raw_score", ascending=False).reset_index(drop=True)
    summary = _score_summary(scored_df)

    return {
        "filename": f"scored_{file.filename}",
        "required_columns": list(df.columns),
        "summary": summary,
        "preview_rows": _preview_rows(scored_df),
        "csv_base64": _dataframe_to_csv_base64(scored_df),
    }


@app.post("/api/outreach")
async def api_generate_outreach(
    file: UploadFile = File(...),
    generate_all: bool = Form(True),
    top_n: int = Form(50),
    delay_seconds: float = Form(1.0),
) -> Dict[str, Any]:
    """Generate outreach for a scored CSV and return enriched results."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(
            status_code=400,
            detail="ANTHROPIC_API_KEY is not configured. Outreach generation requires it.",
        )

    df = _load_csv_from_upload(file)
    if "raw_score" not in df.columns or "score_explanation" not in df.columns:
        raise HTTPException(
            status_code=400,
            detail="Please upload a scored CSV generated by score_leads.py or /api/score.",
        )

    if top_n < 1:
        raise HTTPException(status_code=400, detail="top_n must be at least 1.")
    if delay_seconds < 0:
        raise HTTPException(status_code=400, detail="delay_seconds cannot be negative.")

    scored_rows = df.sort_values("raw_score", ascending=False).reset_index(drop=True).to_dict("records")
    requested_top_n = None if generate_all else top_n
    enriched_rows = generate_outreach_batch(
        scored_rows,
        top_n=requested_top_n,
        delay_seconds=delay_seconds,
    )
    outreach_df = pd.DataFrame(enriched_rows)

    generated_count = int((outreach_df["outreach_status"] == "generated").sum()) if not outreach_df.empty else 0
    failed_count = int(len(outreach_df) - generated_count)

    return {
        "filename": f"outreach_{file.filename}",
        "generated_count": generated_count,
        "failed_count": failed_count,
        "preview_rows": _preview_rows(outreach_df),
        "csv_base64": _dataframe_to_csv_base64(outreach_df),
    }
