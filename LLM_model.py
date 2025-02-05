from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage

local_llm = "codellama:13b"
base_url = "http://smart4lm.llm.solent.fr:11434/"

llm = OllamaLLM(
    model=local_llm,
    base_url=base_url,
    temperature=0.3,  # Allows slight randomness
    top_p=0.9  # Ensures balanced diversity in generation
)

# Clearer system instruction
instruction = (
    "You are an expert in mathematical modeling and system dynamics. "
    "Your task is to generate Python code for a system, based on some phrases and variables."
    "Ensure the code is efficient, well-structured, and follows best practices in scientific computing."
)

# Well-structured user request
user_prompt = (
    "Write me a code in python to run write partial differential equations as:\n"
    "dM_dt = self.r_m * S - self.r_nr * M - self.r_ref * M - self.r_k * M\n"
    "And use Numpy and Scipy functions to solve the system"
)

# Invoke LLM
result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])

print(result)
