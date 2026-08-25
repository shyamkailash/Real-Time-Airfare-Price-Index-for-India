from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CollectionSummary:
    total_sources: int
    successful_sources: int
    failed_sources: int
    total_collected: int
    duplicates_skipped: int
    new_records_stored: int
    started_at: datetime
    completed_at: datetime
