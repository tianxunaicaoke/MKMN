from typing import Any, Dict, List, Callable, Tuple

from langchain import ConversationChain, LLMChain
from langchain.chains.base import Chain
from langchain.schema import BaseMemory
from pydantic import Field

from memories import HumanFeedbackBufferMemory, ContextMemory


class HumanFeedbackChain(ConversationChain):
    memory: BaseMemory = Field(default_factory=HumanFeedbackBufferMemory)
    feedback_prefix: str = 'Answer:'
    question_prefix: str = 'Question:'
    is_finished: bool = False

    def run(self, *args: Any, **kwargs: Any) -> str:
        return self.__extract_question(super().run(**self.__prep_input(*args, **kwargs)))

    def __prep_input(self, *args: Any, **kwargs: Any):
        merged = {'stop': f"\n{self.feedback_prefix}", **kwargs}
        if args:
            merged = {self.input_key: args[0], **merged}
        if merged and merged[self.input_key]:
            merged[self.input_key] = f"{self.feedback_prefix}{merged[self.input_key]}\n"
        return merged

    def __extract_question(self, response):
        index = response.rfind(f"\n{self.question_prefix}")
        if index != -1:
            return response[index + len(f"\n{self.question_prefix}"):]
        else:
            self.is_finished = True
            return response


class ConvergentDivergentChain(Chain):
    memory: BaseMemory
    convergent: HumanFeedbackChain
    divergent: LLMChain
    output_key: str = "response"
    convergent_result_key: str = "divergent_result"

    @property
    def input_keys(self) -> List[str]:
        if self.convergent.is_finished:
            return self.divergent.input_keys
        else:
            return self.convergent.input_keys

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        if not self.convergent.is_finished:
            response = self.convergent.run(**inputs)
            if self.convergent.is_finished:
                self.memory.save_context({self.convergent_result_key: response}, {})
        else:
            response = self.divergent.run(**inputs)
        return {self.output_key: response}
