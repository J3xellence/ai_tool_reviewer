import gradio as gr
import os
import zipfile
import logging
from datetime import datetime

import config
from agents.scraping_agent import scrape_tool_info
from agents.testing_agent import test_tool_api
from agents.evaluation_agent import evaluate_tool
from agents.content_agent import generate_review

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_review(tool_input, screenshots):
    # 1. Scrape info
    info = scrape_tool_info(tool_input)
    tool_info_md = f"# Tool Info: {info.get('Name', tool_input)}\n\n"
    for k, v in info.items():
        if v:
            tool_info_md += f"**{k}:** {v}\n\n"
    # 2. Test API
    test_md = test_tool_api(tool_input, info)
    test_results_md = f"## Test Results for {tool_input}\n\n{test_md}"
    # 3. Evaluate
    eval_md = evaluate_tool(tool_input, info, test_md)
    evaluation_md = f"## Evaluation\n\n{eval_md}"
    # 4. Generate review
    full_md = generate_review(tool_input, tool_info_md, test_results_md, evaluation_md)
    full_review_md = f"# Full Review\n\n{full_md}"
    # 5. Bundle into ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = "".join(ch for ch in info.get("Name", tool_input) if ch.isalnum() or ch in (" ", "_")).strip()
    zip_fn = f"{name}_{timestamp}.zip"
    zip_path = os.path.join(os.getcwd(), zip_fn)
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("tool_info.md", tool_info_md)
        zf.writestr("test_results.md", test_results_md)
        zf.writestr("evaluation.md", evaluation_md)
        zf.writestr("full_review.md", full_review_md)
        if screenshots:
            if isinstance(screenshots, list):
                for f in screenshots:
                    zf.write(f.name, arcname=os.path.basename(f.name))
            else:
                zf.write(screenshots.name, arcname=os.path.basename(screenshots.name))
    return tool_info_md, test_results_md, full_review_md, zip_path

with gr.Blocks() as demo:
    gr.Markdown("## AI Tool Reviewer 🚀")
    with gr.Row():
        inp = gr.Textbox(lines=1, label="Tool Name or URL")
        files = gr.File(file_count="multiple", label="Upload Screenshots")
    btn = gr.Button("Run Review")
    with gr.Tab("Tool Info"):
        out1 = gr.Markdown()
    with gr.Tab("Test Results"):
        out2 = gr.Markdown()
    with gr.Tab("Full Review"):
        out3 = gr.Markdown()
    download = gr.File(label="Download ZIP")
    btn.click(run_review, inputs=[inp, files], outputs=[out1, out2, out3, download])

demo.launch(share=True)
