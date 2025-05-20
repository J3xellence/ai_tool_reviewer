from huggingface_hub import InferenceClient
import logging

logging.basicConfig(level=logging.INFO)
hf_logger = logging.getLogger(__name__)

class HuggingFaceClient:
    """
    Wrapper for Hugging Face Inference API calls.
    """
    def __init__(self, model_id: str, token: str):
        self.client = InferenceClient(model=model_id, token=token)

    def generate(self, messages, max_tokens=512):
        try:
            response = self.client.chat_completion(messages, max_tokens=max_tokens)
            return response.choices[0].message.content
        except Exception as e:
            hf_logger.error(f"HuggingFace API call failed: {e}")
            return ""
