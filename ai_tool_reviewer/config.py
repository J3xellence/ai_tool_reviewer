# Configuration file for tokens and other settings.

# Hugging Face Access Token (replace placeholder with your token)
HF_TOKEN = "> place your Hugging Face access token here <"

# Optionally, add other tokens (e.g., SERPAPI for Google search, if used):
SERPAPI_API_KEY = "> place your SERPAPI key here <"

# Model IDs for tasks (could be customized)
MODEL_IDS = {
    "analysis": "mistralai/Mistral-7B-Instruct-v0.1",    # analytical tasks
    "summarize": "mistralai/Mixtral-8x7B-Instruct-v0.1", # summarization / coding
    "creative": "mistralai/Zephyr-7B-Base"               # creative writing
}
