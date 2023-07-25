import gradio as gr

from memories import ContextMemory
from tasking.chain import create_chain


def enable_tasking(architecture):
    context_memory = ContextMemory()
    with gr.Tab("Tasking"):
        with gr.Row():
            with gr.Column(scale=0.5):
                tasking_chatbot = gr.Chatbot(label="Assistant").style(height=650)
                message = gr.Textbox(label="Clarification")
            with gr.Column(scale=0.5):
                user_story = gr.Textbox(label="User story", lines=5)
                architecture = gr.Code(architecture, language="markdown", interactive=True, lines=29,
                                       label="Architecture")
                tasking = gr.Button("Tasking")

        chain = create_chain(context_memory)

        def start(story: str, context: str):
            nonlocal chain
            chain.memory.clear()
            chain = create_chain(context_memory)
            context_memory.save_context({'requirements': story, 'context': context}, {})
            response = chain.run('')
            return "", [("Tasking:", response)]

        def chat(message: str, history):
            response = chain.run(message)
            history.append((message, response))
            return "", history

        tasking.click(start, [user_story, architecture], [message, tasking_chatbot])
        message.submit(chat, [message, tasking_chatbot], [message, tasking_chatbot])
