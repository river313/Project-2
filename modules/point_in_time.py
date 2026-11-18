#!/usr/bin/env python3
"""
================================================================================
FIN 439: Applied Financial Modeling & Corporate Valuation
Project 2: Investment Management Application
Student: Elliot
Module: modules/point_in_time.py

Description:
    Point-in-time macroeconomic and interest rate data pipeline.
    Reused from Lab 16 (provenance filtering) and Lab 17 (FRED/ALFRED live downloads).
    Enforces strict temporal hygiene to eliminate look-ahead bias:
      1. Distinguishes event time, publication date, and revision date.
      2. Downloads current time series from FRED and historical vintages from ALFRED.
      3. Implements the 10-Year Treasury Yield (DGS10) point-in-time signal
         and provides verification against professor's known answers (Oct 5, 2026).
================================================================================
"""

from __future__ import annotations

import io
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd

try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    import requests as std_requests
    HAS_CURL_CFFI = False

# ==============================================================================
# DATA RETRIEVAL (FRED & ALFRED PUBLIC ENDPOINTS)
# ==============================================================================

def fetch_url_text(url: str, timeout: int = 30) -> str:
    """Fetch text content from a URL using curl_cffi (Chrome impersonation) or requests."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    if HAS_CURL_CFFI:
        resp = cffi_requests.get(url, impersonate="chrome", timeout=timeout)
    else:
        resp = std_requests.get(url, headers=headers, timeout=timeout)

    if resp.status_code != 200:
        raise ValueError(f"HTTP {resp.status_code}: Failed to download from {url}")

    text = resp.text
    if text.strip().startswith("<!DOCTYPE") or text.strip().startswith("<html"):
        raise ValueError(f"Invalid series or error page returned from {url}")

    return text


def parse_fred_csv(csv_text: str, series_id: str) -> pd.DataFrame:
    """Parse raw FRED/ALFRED CSV text, handling '.' missing values and dates."""
    df = pd.read_csv(io.StringIO(csv_text))
    if df.empty or len(df.columns) < 2:
        raise ValueError(f"Malformed or empty dataset returned for series '{series_id}'")

    date_col = df.columns[0]
    val_col = df.columns[1]

    # Filter out missing '.' values
    df = df[df[val_col] != "."].copy()
    if df.empty:
        raise ValueError(f"No valid non-missing observations found for series '{series_id}'")

    df["observation_date"] = pd.to_datetime(df[date_col])
    df["value"] = pd.to_numeric(df[val_col])
    df = df.sort_values(by="observation_date").reset_index(drop=True)
    return df[["observation_date", "value"]]


def download_fred_current(series_id: str) -> pd.DataFrame:
    """Download current time series data from FRED."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    csv_text = fetch_url_text(url)
    return parse_fred_csv(csv_text, series_id)


def download_alfred_vintage(series_id: str, vintage_date: str) -> pd.DataFrame:
    """Download historical vintage data from ALFRED as known on vintage_date."""
    url = f"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage_date}"
    csv_text = fetch_url_text(url)
    return parse_fred_csv(csv_text, series_id)


# ==============================================================================
# POINT-IN-TIME RECONCILIATION & AUDIT
# ==============================================================================

def audit_point_in_time_series(series_id: str, vintage_date_str: str) -> Dict[str, Any]:
    """
    Compares the historical vintage of a series known on vintage_date_str
    against the current series downloaded today.
    Returns:
      - Last date & value known on cutoff date
      - Latest date & value today
      - Count of observations published after cutoff
      - Count of revisions to matching historical dates
    """
    df_curr = download_fred_current(series_id)
    df_vint = download_alfred_vintage(series_id, vintage_date_str)

    if df_vint.empty:
        raise ValueError(f"No vintage data available for {series_id} as of {vintage_date_str}")

    last_vint_row = df_vint.iloc[-1]
    last_vint_date = last_vint_row["observation_date"]
    last_vint_val = float(last_vint_row["value"])

    last_curr_row = df_curr.iloc[-1]
    last_curr_date = last_curr_row["observation_date"]
    last_curr_val = float(last_curr_row["value"])

    # Count observations added after cutoff date
    cutoff_ts = pd.to_datetime(vintage_date_str)
    added_after = int((df_curr["observation_date"] > cutoff_ts).sum())

    # Check for revisions on dates present in both sets
    merged = pd.merge(df_vint, df_curr, on="observation_date", suffixes=("_vint", "_curr"))
    revised_count = int((merged["value_vint"] != merged["value_curr"]).sum())

    return {
        "series_id": series_id,
        "vintage_date": vintage_date_str,
        "last_vint_date": last_vint_date.strftime("%Y-%m-%d"),
        "last_vint_value": last_vint_val,
        "latest_curr_date": last_curr_date.strftime("%Y-%m-%d"),
        "latest_curr_value": last_curr_val,
        "observations_added_after": added_after,
        "observations_revised": revised_count,
    }


def verify_dgs10_known_answer() -> Dict[str, Any]:
    """
    Verifies 10-Year Treasury Yield (DGS10) against professor's known answers
    as of October 5, 2026:
      - Expected last date known: October 2, 2026 (2026-10-02)
      - Expected value known: 5.28%
    """
    audit = audit_point_in_time_series("DGS10", "2026-10-05")
    pass_date = audit["last_vint_date"] == "2026-10-02"
    pass_val = abs(audit["last_vint_value"] - 5.28) < 1e-2

    return {
        "series_id": "DGS10",
        "audit": audit,
        "passed": pass_date and pass_val,
        "expected_date": "2026-10-02",
        "expected_value": 5.28,
    }
