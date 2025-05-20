import logging
import config
from smolagents import CodeAgent, HfApiModel

logger = logging.getLogger(__name__)

def evaluate_tool(tool_input: str, info: dict, test_results: str):
    """
    Analyze strengths/weaknesses using an LLM based on info and test results.
    """
    analysis_md = ""
    try:
        agent = CodeAgent(
            tools=[],
            model=HfApiModel(config.MODEL_IDS["analysis"], token=config.HF_TOKEN),
            verbose=False
        )
        prompt = (
            f"Analyze the strengths and weaknesses of the tool '{tool_input}'. "
            f"Tool Info: {info}\nTest Results: {test_results}"
        )
        analysis_md = agent.run(prompt)
    except Exception as e:
        logger.error(f"Error in evaluation agent: {e}")
        analysis_md = f"Error in evaluation: {e}"
    return analysis_md
