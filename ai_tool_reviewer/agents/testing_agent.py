import logging
import config
from smolagents import CodeAgent, HfApiModel

logger = logging.getLogger(__name__)

def test_tool_api(tool_input: str, info: dict):
    """
    Identify and attempt to test any public APIs of the tool.
    Returns a markdown string summarizing test results.
    """
    results_md = "No public API found or no tests executed."
    try:
        agent = CodeAgent(
            tools=[],
            model=HfApiModel(config.MODEL_IDS["analysis"], token=config.HF_TOKEN),
            verbose=False
        )
        prompt = (
            f"Given the following information about a tool, identify any public HTTP APIs "
            f"and write Python `requests` code to call an example endpoint. Tool info: {info}"
        )
        agent_output = agent.run(prompt)
        results_md = f"```python
# Suggested code and output by agent:\n{agent_output}\n```"
    except Exception as e:
        logger.error(f"Error in testing agent: {e}")
        results_md = f"Error testing tool APIs: {e}"
    return results_md
