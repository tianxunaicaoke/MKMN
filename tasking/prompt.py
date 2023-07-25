from langchain import PromptTemplate

TASKING = """
You are a software developer. I'm the software architect.

===CONTEXT
{context}
===END OF CONTEXT

===REQUIREMENTS
{requirements}
===END REQUIREMENTS

Tasking for each acceptance criteria to complete the requirements according to the architecture description and the working processes. 
Each acceptance criteria should be broken down into tasks according to the architecture description and the working processes.
Each task can correspond to a working process, but not every working process is necessary when complete an acceptance criteria, so you should only list the necessary tasks and indicate the correspond working process. 
Use the following format:

Acceptance Criteria 1: the first acceptance criteria in the requirements
Tasks: all necessary tasks to complete the acceptance criteria, each task should be described briefly and associated with a working process.
Task 1: the concrete task to complete the acceptance criteria. [Working Process A]
Task 2: the concrete task to complete the acceptance criteria. [Working Process B]
Task 3: the concrete task to complete the acceptance criteria. [Working Process C]

Acceptance Criteria 2: the second acceptance criteria in the requirements
Tasks: all necessary tasks to complete the acceptance criteria, each task should be described briefly and associated with a working process.
Task 1: the concrete task to complete the acceptance criteria. [Working Process A]
Task 2: the concrete task to complete the acceptance criteria. [Working Process B]
Task 3: the concrete task to complete the acceptance criteria. [Working Process C]

and so on.
Don't generated code! Follow the above architecture to think about the solution to complete the acceptance criteria and tasking for it.

{history}
{input}"""

CONVERSATION = """
You are a software developer. I'm the software architect.

===CONTEXT
{context}
===END OF CONTEXT

===REQUIREMENTS
{requirements}
===END REQUIREMENTS

===SOLUTIONS
{solutions}
===END SOLUTIONS

current conversations:
{history}
Human:{input}
AI:"""

_template = """
You are a software developer. I'm the software architect.
Here are the architecture of the current system describe in mermaid flowchart 

===ARCHITECTURE
{context}
===END ARCHITECTURE

And the current requirements in user story and scenarios

===REQUIREMENTS
{requirements}
===END REQUIREMENTS

Don't generated code! Follow the above architecture, describe a detailed solution for the given requirements.


current conversation:
{history}
Human: {input}
AI:"""

tasking_template = PromptTemplate(
    input_variables=["context", "requirements", "history", "input"],
    template=TASKING
)

conversation_template = PromptTemplate(
    input_variables=["context", "requirements", "solutions", "history", "input"],
    template=CONVERSATION
)
