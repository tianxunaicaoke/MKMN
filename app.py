import gradio as gr

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from acceptances.ui import enable_acceptances
from tasking.ui import enable_tasking

with open('documents/business_context.md', 'r') as file:
    business_context = file.read()
with open('documents/architecture.md', 'r') as file:
    architecture = file.read()

with gr.Blocks() as ui:
    enable_acceptances(business_context)
    enable_tasking(architecture)

ui.launch(debug=True)
