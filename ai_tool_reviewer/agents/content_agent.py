import logging
import config
from smolagents import CodeAgent, HfApiModel
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

logger = logging.getLogger(__name__)

def generate_review(tool_input: str, info: str, tests: str, analysis: str):
    """
    Combine info, tests, and analysis to generate a full tool review.
    """
    try:
        template = PromptTemplate(
            input_variables=["tool", "info", "tests", "analysis"],
            template=(
                "You are an expert tech reviewer. Write a comprehensive review of '{tool}'.\n"
                "Info:\n{info}\nTests:\n{tests}\nAnalysis:\n{analysis}"
            )
        )
        llm = HuggingFaceHub(
            repo_id=config.MODEL_IDS["creative"],
            huggingfacehub_api_token=config.HF_TOKEN,
            model_kwargs={"temperature": 0.7, "max_length": 1024}
        )
        chain = LLMChain(llm=llm, prompt=template)
        return chain.run(tool=tool_input, info=info, tests=tests, analysis=analysis)
    except Exception as e:
        logger.error(f"Error in content agent: {e}")
        # fallback
        fallback = CodeAgent(
            tools=[],
            model=HfApiModel(config.MODEL_IDS["creative"], token=config.HF_TOKEN),
            verbose=False
        )
        prompt = f"Write a review of '{tool_input}' using: {info}, {tests}, {analysis}"
        return fallback.run(prompt)
