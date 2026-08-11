"""
loader.py

Centralized dataset loader for the Performance Test Agent.

Responsibilities:
1. Load CSV dataset
2. Validate required columns
3. Cache the DataFrame
4. Return a pandas DataFrame

No business logic should exist here.
"""

from pathlib import Path
from functools import lru_cache

import pandas as pd


# ============================================================
# Dataset Configuration
# ============================================================

from pathlib import Path

DATASET_PATH = Path("data/performance_dataset.csv")

REQUIRED_COLUMNS = [
    "Job ID",
    "Scenario",
    "API",
    "Response Time (ms)",
    "HTTP Status",
    "CPU (%)",
    "Memory (%)",
    "DB Connections",
    "SLA",
    "Bottleneck",
    "Recommendation",
]


# ============================================================
# Data Loader
# ============================================================

@lru_cache(maxsize=1)
def load_dataset() -> pd.DataFrame:
    """
    Load and cache the performance dataset.

    Returns:
        pd.DataFrame
    """

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    validate_dataset(df)

    return df


# ============================================================
# Dataset Validation
# ============================================================

def validate_dataset(df: pd.DataFrame) -> None:
    """
    Validate dataset structure.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


# ============================================================
# Utility Functions
# ============================================================

def reload_dataset() -> pd.DataFrame:
    """
    Clear cache and reload dataset.
    Useful during development.
    """

    load_dataset.cache_clear()

    return load_dataset()