from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import CombinedMemory, ConversationBufferMemory

from acceptances.prompts import feedback_template, conversation_template
from chains import HumanFeedbackChain, ConvergentDivergentChain
from memories import MemoryView, HumanFeedbackBufferMemory


def create_chain(context_memory):
    convergent = HumanFeedbackChain(llm=ChatOpenAI(temperature=0.7),
                                    memory=(
                                        CombinedMemory(memories=[HumanFeedbackBufferMemory(input_key="input"),
                                                                 MemoryView(memory=context_memory,
                                                                            variables=['context', 'story'])])),
                                    prompt=feedback_template,
                                    verbose=True)

    divergent = ConversationChain(llm=ChatOpenAI(temperature=0.7),
                                  memory=(
                                      CombinedMemory(memories=[ConversationBufferMemory(input_key="input"),
                                                               MemoryView(memory=context_memory,
                                                                          variables=['context', 'scenarios',
                                                                                     'story'])])),
                                  prompt=conversation_template,
                                  verbose=True)

    return ConvergentDivergentChain(memory=context_memory,
                                    convergent=convergent,
                                    convergent_result_key="scenarios",
                                    divergent=divergent)
