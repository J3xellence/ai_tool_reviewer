# AI Tool Reviewer

This project is a Gradio-based application for **automated reviews of AI tools**. It uses a multi-agent architecture combining [smolagents](https://github.com/huggingface/smolagents) (for planning/scraping/testing/evaluation), [LangChain](https://python.langchain.com) (for model routing and chains), and the [Hugging Face Inference API](https://huggingface.co/docs/huggingface_hub/main/en/inference) (for LLM calls). The UI has tabs for:

- **Tool Info**: scraped documentation and website info
- **Test Results**: outcomes of any public API calls
- **Full Review**: generated review text

Features include:
- Live scraping of GitHub README, website, pricing, etc.
- Optional public-API testing (via `requests` and CodeAgents)
- Content generation using Mixtral/Mistral/Zephyr models via Hugging Face.
- ZIP download of the complete report.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Put your Hugging Face token in `config.py`.
3. Run `python app.py` to start the app (or deploy to Gradio Spaces / Colab).
4. Input a tool name or URL and click “Run Review”. View results and download report.
