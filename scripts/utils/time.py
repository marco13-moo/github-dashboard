from datetime import datetime, timezone

def utc_now():
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)

def parse_github_timestamp(ts: str):
    """
    Parse GitHub ISO timestamps safely.
    Example: 2025-01-06T13:42:11Z
    """
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))
