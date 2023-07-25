import glob
import os
from typing import Any, List, Optional

import gradio as gr
from langchain.document_loaders.unstructured import UnstructuredBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import MarkdownTextSplitter
from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStoreRetriever

from components.markdown import editor

embeddings = OpenAIEmbeddings()

retriever: Optional[VectorStoreRetriever] = None


def get_retriever():
    if retriever is not None:
        return retriever
    return Chroma(embedding_function=embeddings, persist_directory="db").as_retriever()


def load_from(directory: str):
    files = glob.glob(directory + "/*.md")
    knowledge_content = []
    knowledge_files = []
    with gr.Tab("Knowledge base") as ui:
        with gr.Row():
            with gr.Column(scale=0.85):
                indicator = gr.Markdown("")
            with gr.Column(scale=0.15):
                create_index = gr.Button("Create Index")
        with gr.Row():
            with gr.Column():
                for file_path in files:
                    name = os.path.splitext(os.path.basename(file_path))[0]
                    with open(file_path, 'r') as file:
                        content = file.read()
                        if content != "":
                            with gr.Accordion(name, open=False):
                                code, viewer = editor(content)
                                knowledge_content.append(code)
                                knowledge_files.append(name)

        def create(*texts: str):
            loaders = map(lambda text: UnstructuredMarkdownLoader(source="knowledge_base", text=text), texts)
            index = VectorstoreIndexCreator(text_splitter=MarkdownTextSplitter(chunk_size=1000, chunk_overlap=0),
                                            vectorstore_kwargs={"persist_directory": "db", "ids": knowledge_files}) \
                .from_loaders(list(loaders))
            global retriever
            retriever = index.vectorstore.as_retriever()
            return ""

        create_index.click(create, inputs=knowledge_content, outputs=indicator)
        return ui


class UnstructuredMarkdownLoader(UnstructuredBaseLoader):
    def __init__(self, source: str, text: str, mode: str = "single", **unstructured_kwargs: Any):
        self.text = text
        self.source = source
        super().__init__(mode=mode, **unstructured_kwargs)

    def _get_elements(self) -> List:
        from unstructured.__version__ import __version__ as __unstructured_version__
        from unstructured.partition.md import partition_md

        _unstructured_version = __unstructured_version__.split("-")[0]
        unstructured_version = tuple([int(x) for x in _unstructured_version.split(".")])

        if unstructured_version < (0, 4, 16):
            raise ValueError(
                f"You are on unstructured version {__unstructured_version__}. "
                "Partitioning markdown files is only supported in unstructured>=0.4.16."
            )
        return partition_md(text=self.text, **self.unstructured_kwargs)

    def _get_metadata(self) -> dict:
        return {"source": self.source}
