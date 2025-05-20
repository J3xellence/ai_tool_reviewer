import re
import logging
import config
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel
from utils.scraper import fetch_text_from_url

logger = logging.getLogger(__name__)

def scrape_tool_info(tool_input: str):
    """
    Scrape information about the tool from web sources.
    Returns a dictionary of info (e.g., name, description, website, GitHub link).
    """
    info = {
        "Name": tool_input,
        "Description": "",
        "Website": "",
        "GitHub": "",
        "Key Features": "",
        "Pricing": ""
    }

    # If input is a URL, detect domain
    domain = tool_input if re.match(r'^https?://', tool_input) else ""

    try:
        # Search official site if not provided
        if not domain:
            search_agent = CodeAgent(
                tools=[DuckDuckGoSearchTool(max_results=3)],
                model=HfApiModel(config.MODEL_IDS["analysis"], token=config.HF_TOKEN),
                verbose=False
            )
            result = search_agent.run(f"Official website of {tool_input}")
            urls = re.findall(r'https?://[^\s]+', result)
            if urls:
                domain = urls[0]

        if domain:
            logger.info(f"Fetching website content from {domain}")
            content = fetch_text_from_url(domain)
            lines = content.splitlines()
            # Description: first substantial line
            for line in lines:
                if len(line.strip()) > 50:
                    info["Description"] = line.strip()
                    break
            # Key features: lines starting with bullet chars
            features = [ln.strip() for ln in lines if ln.strip().startswith(("-", "*"))][:5]
            info["Key Features"] = "\n".join(features)
            info["Website"] = domain

            # Pricing page heuristic
            pricing_url = domain.rstrip("/") + "/pricing"
            prices_text = fetch_text_from_url(pricing_url, max_chars=2000)
            if "pricing" in prices_text.lower():
                info["Pricing"] = prices_text[:200] + "..."

        # GitHub search
        if not info["GitHub"]:
            gh_search_agent = CodeAgent(
                tools=[DuckDuckGoSearchTool(max_results=2)],
                model=HfApiModel(config.MODEL_IDS["analysis"], token=config.HF_TOKEN),
                verbose=False
            )
            gh_result = gh_search_agent.run(f"{tool_input} GitHub repository")
            gh_urls = re.findall(r'https?://github.com/[^\s]+', gh_result)
            if gh_urls:
                info["GitHub"] = gh_urls[0].split()[0]
    except Exception as e:
        logger.error(f"Error in scraping agent: {e}")

    return info
