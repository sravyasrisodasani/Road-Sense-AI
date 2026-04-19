import requests

def is_online() -> bool:
    """Check internet connectivity by pinging a lightweight endpoint."""
    try:
        requests.get("https://nominatim.openstreetmap.org", timeout=3)
        return True
    except Exception:
        return False
