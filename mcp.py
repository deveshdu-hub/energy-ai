#!/usr/bin/env python3
"""
energy_ai_mcp — MCP server for Energy AI (futurehq.in)

Connects Claude to the Energy AI Supabase backend: leads, stats,
pincode analytics, and vendor-ready summaries.

Env vars required:
    SUPABASE_URL  — e.g. https://xxxx.supabase.co
    SUPABASE_KEY  — service_role or anon key with access to the tables

Run (stdio, for Claude Desktop):
    python energy_ai_mcp.py
"""

import json
import os
from collections import Counter
from enum import Enum
from typing import Any, Dict, List, Optional

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field, field_validator

# ─── CONFIG ────────────────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
LEADS_TABLE = os.getenv("ENERGY_AI_LEADS_TABLE", "leads")
TIMEOUT = 15.0

mcp = FastMCP("energy_ai_mcp")


# ─── SHARED HELPERS ────────────────────────────────────────────────
def _headers() -> Dict[str, str]:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _check_config() -> Optional[str]:
    if not SUPABASE_URL or not SUPABASE_KEY:
        return (
            "Error: SUPABASE_URL and SUPABASE_KEY environment variables are not set. "
            "Add them to the MCP server config (same values used in Streamlit secrets)."
        )
    return None


async def _rest_get(path: str, params: Dict[str, Any]) -> Any:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.get(f"{SUPABASE_URL}/rest/v1/{path}", params=params, headers=_headers())
        r.raise_for_status()
        return r.json()


async def _rest_post(path: str, payload: Dict[str, Any]) -> Any:
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.post(f"{SUPABASE_URL}/rest/v1/{path}", json=payload, headers=_headers())
        r.raise_for_status()
        return r.json()


def _handle_error(e: Exception) -> str:
    if isinstance(e, httpx.HTTPStatusError):
        code = e.response.status_code
        if code == 401:
            return "Error: Supabase rejected the key (401). Check SUPABASE_KEY."
        if code == 404:
            return (
                f"Error: table '{LEADS_TABLE}' not found (404). "
                "Create it in Supabase (see README SQL) or set ENERGY_AI_LEADS_TABLE."
            )
        if code == 429:
            return "Error: Supabase rate limit hit (429). Wait a moment and retry."
        return f"Error: Supabase request failed with HTTP {code}: {e.response.text[:200]}"
    if isinstance(e, httpx.TimeoutException):
        return "Error: Supabase request timed out. Check SUPABASE_URL and network."
    return f"Error: {type(e).__name__}: {e}"


def _fmt_lead_md(lead: Dict[str, Any]) -> str:
    name = lead.get("name", "Unknown")
    return (
        f"- **{name}** | 📱 {lead.get('mobile', '—')} | 📍 {lead.get('pincode', '—')} "
        f"| ⚡ {lead.get('service', '—')} | score {lead.get('score', '—')} "
        f"| {lead.get('created_at', '')[:16]}"
    )


class ResponseFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"


# ─── TOOL 1: LIST LEADS ────────────────────────────────────────────
class ListLeadsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    service: Optional[str] = Field(
        default=None,
        description="Filter by service type, e.g. 'Solar', 'EV Charging'. Omit for all services.",
        max_length=60,
    )
    pincode: Optional[str] = Field(
        default=None, description="Filter by exact 6-digit Indian pincode, e.g. '700001'.",
        pattern=r"^\d{6}$",
    )
    min_score: Optional[int] = Field(
        default=None, description="Only leads with score >= this value (lead quality filter).",
        ge=0, le=100,
    )
    limit: int = Field(default=20, description="Max leads to return (1-100).", ge=1, le=100)
    offset: int = Field(default=0, description="Rows to skip, for pagination.", ge=0)
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="'markdown' for human-readable, 'json' for full structured data.",
    )


@mcp.tool(
    name="energyai_list_leads",
    annotations={
        "title": "List Energy AI Leads",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def energyai_list_leads(params: ListLeadsInput) -> str:
    """List citizen leads captured by the Energy AI app, newest first.

    Supports filtering by service type, pincode, and minimum lead score,
    with limit/offset pagination.

    Returns:
        str: Markdown list of leads, or JSON with keys:
             {count, offset, has_more, leads: [{name, mobile, pincode, service, score, created_at}]}
    """
    if err := _check_config():
        return err
    try:
        query: Dict[str, Any] = {
            "select": "*",
            "order": "created_at.desc",
            "limit": params.limit + 1,
            "offset": params.offset,
        }
        if params.service:
            query["service"] = f"ilike.*{params.service}*"
        if params.pincode:
            query["pincode"] = f"eq.{params.pincode}"
        if params.min_score is not None:
            query["score"] = f"gte.{params.min_score}"

        rows: List[Dict] = await _rest_get(LEADS_TABLE, query)
        has_more = len(rows) > params.limit
        rows = rows[: params.limit]

        if params.response_format == ResponseFormat.JSON:
            return json.dumps(
                {"count": len(rows), "offset": params.offset, "has_more": has_more, "leads": rows},
                indent=2, default=str,
            )
        if not rows:
            return "No leads found for these filters. Try removing filters or check back after new citizen signups."
        lines = [f"## Energy AI Leads ({len(rows)} shown{', more available' if has_more else ''})\n"]
        lines += [_fmt_lead_md(l) for l in rows]
        return "\n".join(lines)
    except Exception as e:
        return _handle_error(e)


# ─── TOOL 2: LEAD STATS ────────────────────────────────────────────
class LeadStatsInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sample_size: int = Field(
        default=500, description="How many recent leads to analyze (1-1000).", ge=1, le=1000
    )


@mcp.tool(
    name="energyai_lead_stats",
    annotations={
        "title": "Energy AI Lead Statistics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def energyai_lead_stats(params: LeadStatsInput) -> str:
    """Aggregate statistics over recent Energy AI leads.

    Computes total analyzed, breakdown by service, top pincodes,
    average lead score, and share of high-quality leads (score >= 70).

    Returns:
        str: Markdown stats report.
    """
    if err := _check_config():
        return err
    try:
        rows: List[Dict] = await _rest_get(
            LEADS_TABLE,
            {"select": "service,pincode,score,created_at", "order": "created_at.desc",
             "limit": params.sample_size},
        )
        if not rows:
            return "No leads in the database yet. Stats will appear once citizens start signing up."

        services = Counter(r.get("service") or "Unknown" for r in rows)
        pincodes = Counter(r.get("pincode") or "Unknown" for r in rows)
        scores = [r["score"] for r in rows if isinstance(r.get("score"), (int, float))]
        avg = sum(scores) / len(scores) if scores else 0
        hot = sum(1 for s in scores if s >= 70)

        out = [f"## Energy AI Lead Stats (last {len(rows)} leads)\n"]
        out.append(f"**Average score:** {avg:.1f} | **Hot leads (≥70):** {hot} "
                   f"({hot * 100 // max(len(scores), 1)}%)\n")
        out.append("**By service:**")
        out += [f"- {s}: {c}" for s, c in services.most_common()]
        out.append("\n**Top pincodes:**")
        out += [f"- {p}: {c} leads" for p, c in pincodes.most_common(5)]
        return "\n".join(out)
    except Exception as e:
        return _handle_error(e)


# ─── TOOL 3: SEARCH LEADS ──────────────────────────────────────────
class SearchLeadsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    query: str = Field(
        ..., description="Name fragment or mobile number fragment to search, e.g. 'Sharma' or '98300'.",
        min_length=2, max_length=60,
    )
    limit: int = Field(default=20, ge=1, le=100, description="Max results.")


@mcp.tool(
    name="energyai_search_leads",
    annotations={
        "title": "Search Energy AI Leads",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def energyai_search_leads(params: SearchLeadsInput) -> str:
    """Search leads by citizen name or mobile number (partial match, case-insensitive).

    Returns:
        str: Markdown list of matching leads with name, mobile, pincode, service, score.
    """
    if err := _check_config():
        return err
    try:
        rows: List[Dict] = await _rest_get(
            LEADS_TABLE,
            {"select": "*", "or": f"(name.ilike.*{params.query}*,mobile.ilike.*{params.query}*)",
             "order": "created_at.desc", "limit": params.limit},
        )
        if not rows:
            return f"No leads matching '{params.query}'. Try a shorter fragment."
        return "\n".join([f"## Matches for '{params.query}' ({len(rows)})\n"]
                         + [_fmt_lead_md(l) for l in rows])
    except Exception as e:
        return _handle_error(e)


# ─── TOOL 4: ADD LEAD ──────────────────────────────────────────────
class AddLeadInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., description="Citizen full name.", min_length=2, max_length=100)
    mobile: str = Field(..., description="10-digit Indian mobile number.", pattern=r"^\d{10}$")
    pincode: str = Field(..., description="6-digit Indian pincode.", pattern=r"^\d{6}$")
    service: str = Field(..., description="Service interest, e.g. 'Solar', 'EV Charging'.",
                         min_length=2, max_length=60)
    score: int = Field(default=50, description="Lead score 0-100 (default 50).", ge=0, le=100)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()


@mcp.tool(
    name="energyai_add_lead",
    annotations={
        "title": "Add Energy AI Lead",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def energyai_add_lead(params: AddLeadInput) -> str:
    """Insert a new lead into the Energy AI database (e.g. from a phone call or WhatsApp inquiry).

    Returns:
        str: Confirmation with the stored record, or an actionable error.
    """
    if err := _check_config():
        return err
    try:
        created = await _rest_post(LEADS_TABLE, params.model_dump())
        rec = created[0] if isinstance(created, list) and created else params.model_dump()
        return f"✅ Lead added:\n{_fmt_lead_md(rec)}"
    except Exception as e:
        return _handle_error(e)


# ─── TOOL 5: PINCODE REPORT ────────────────────────────────────────
class PincodeReportInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    pincode: str = Field(..., description="6-digit pincode to report on, e.g. '700091'.",
                         pattern=r"^\d{6}$")


@mcp.tool(
    name="energyai_pincode_report",
    annotations={
        "title": "Energy AI Pincode Report",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def energyai_pincode_report(params: PincodeReportInput) -> str:
    """Vendor-ready demand report for one pincode: lead count, services requested, average score.

    Useful for pitching the ₹5,000 lead package to local vendors.

    Returns:
        str: Markdown report for the pincode.
    """
    if err := _check_config():
        return err
    try:
        rows: List[Dict] = await _rest_get(
            LEADS_TABLE,
            {"select": "service,score,created_at", "pincode": f"eq.{params.pincode}",
             "order": "created_at.desc", "limit": 500},
        )
        if not rows:
            return (f"No leads yet for pincode {params.pincode}. "
                    "This area is untapped — could be a content-marketing target.")
        services = Counter(r.get("service") or "Unknown" for r in rows)
        scores = [r["score"] for r in rows if isinstance(r.get("score"), (int, float))]
        avg = sum(scores) / len(scores) if scores else 0
        out = [f"## Demand Report — Pincode {params.pincode}\n",
               f"**Total leads:** {len(rows)} | **Avg score:** {avg:.1f}\n",
               "**Services requested:**"]
        out += [f"- {s}: {c}" for s, c in services.most_common()]
        out.append(f"\n**Latest lead:** {rows[0].get('created_at', '')[:16]}")
        return "\n".join(out)
    except Exception as e:
        return _handle_error(e)


if __name__ == "__main__":
    mcp.run()
