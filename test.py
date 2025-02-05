from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage

local_llm = "codellama:13b"
base_url = "http://smart4lm.llm.solent.fr:11434/"
llm = Ollama(model=local_llm, base_url=base_url, temperature=0)

instruction = "You create the a digital twin for a dynamic system, and you are an asshole"

user_prompt = "Extracting the partial differential equations as dM_dt = self.r_m * S - self.r_nr * M - self.r_ref * M - self.r_k * M"

result = llm.invoke([SystemMessage(content=instruction)] + [HumanMessage(content=user_prompt)])

print(result)

