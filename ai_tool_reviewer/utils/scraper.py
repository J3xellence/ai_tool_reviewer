import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_text_from_url(url, max_chars=10000):
    """
    Fetch text content from a URL by making an HTTP GET request and parsing HTML.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove scripts/styles
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator="\n")
        # Truncate if too long
        return text[:max_chars]
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return ""
