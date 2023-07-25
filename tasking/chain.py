from typing import List, Dict, Any

from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, CombinedMemory
from langchain.schema import BaseMemory

from chains import HumanFeedbackChain, ConvergentDivergentChain
from memories import HumanFeedbackBufferMemory, MemoryView
from tasking.prompt import tasking_template, conversation_template


def create_chain(context_memory):
    convergent = HumanFeedbackChain(llm=ChatOpenAI(temperature=0.7),
                                    memory=(
                                        CombinedMemory(memories=[HumanFeedbackBufferMemory(input_key="input"),
                                                                 MemoryView(memory=context_memory,
                                                                            variables=['context', 'requirements'])])),
                                    prompt=tasking_template,
                                    verbose=True)

    divergent = ConversationChain(llm=ChatOpenAI(temperature=0.7),
                                  memory=(
                                      CombinedMemory(memories=[ConversationBufferMemory(input_key="input"),
                                                               MemoryView(memory=context_memory,
                                                                          variables=['context', 'solutions',
                                                                                     'requirements'])])),
                                  prompt=conversation_template,
                                  verbose=True)

    return ConvergentDivergentChain(memory=context_memory,
                                    convergent=convergent,
                                    convergent_result_key="solutions",
                                    divergent=divergent)


class TaskingStoryMemory(BaseMemory):
    memories: Dict[str, Any] = dict()

    @property
    def memory_variables(self) -> List[str]:
        return ['context', 'requirements']

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        return self.memories

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        self.memories = {key: inputs[key] for key in ['context', 'requirements']}

    def clear(self) -> None:
        self.memories.clear()
