import os
import subprocess
import docx
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage

# Define directories
base_dir = os.getcwd()
reports_dir = os.path.join(base_dir, "reports")
approche_dir = os.path.join(base_dir, "approche_systemique")

# Ensure output directory exists
os.makedirs(approche_dir, exist_ok=True)

def extract_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_text_from_docx(docx_path):
    """Extracts raw text from a .docx file"""
    try:
        doc = docx.Document(docx_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
        return ""

def generate_simplified_text(department):
    """
    First LLM: Generates {department}.txt from {department}_report.docx
    """
    docx_path = os.path.join(reports_dir, f"{department}_report.docx")
    txt_output_path = os.path.join(reports_dir, f"{department}.txt")
    example_docx_path = os.path.join(reports_dir, "example_report.docx")
    example_txt = os.path.join(reports_dir, "example.txt")

    if not os.path.exists(docx_path):
        print(f"Error: {docx_path} not found.")
        return

    report_text = extract_text_from_docx(docx_path)
    example_docx = extract_text_from_docx(example_docx_path)
    example_txt = extract_text(example_txt)

    llm = OllamaLLM(
        # model="lllama3.1:8b",
        model="llama3.3:latest",
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.2,
        top_p=0.9)
    
    instruction = (
        "You are an expert in summarization and technical writing. "
        "You are an expert to document the elements of dynamic systems. "
        "Your task is to extract the key details and simplify the content from a long report. "
        "Your task is to separate the different phases and find the input and output values for each. "
        "Maintain the most important technical details while making it concise."
    )

    user_prompt = (
        f"Summarize the following report for the **{department}** department.\n"
        "In the report there are different phases/sections, each has one or more input and output values.\n"
        "Write the name of each phase/seciton and the input and output values for each under it.\n"
        "Output of each phase/section, is the input of the next phase/section.\n"
        "The values of the outputs should be declared as a rate smalle or equal to 1.\n"
        "At each phase, the outputs sum up to 1.\n"
        "If you can't find a value for an output, you may compute it as the difference between 1 and the sum of the other outputs.\n\n"
        "If there are more than one unknown value for outputs, you may choose the values that make the most sense, or use equal values for them.\n\n"
        "Every phase should be connected to the previous phase, and the output of the last phase should be the output of the system.\n\n"
        "Find the input and output values for each phase/section in the report.\n\n"
        "If you don't find a value/rate between two phases, you may assume it a resaosnable value.\n\n"
        f"Similar to tge example {example_txt}, return a document in which, there are only quantitative values of rates for inputs and outputs of each phase and not extra qualitative information.\n\n"
        f"As an example, {example_txt} is generated from {example_docx} and you may do the same for {report_text}.\n\n"
        "Provide the cleaned and simplified text without any extra text."
    )

    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])

    # Strip extra whitespace
    result = result.strip()

    with open(txt_output_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Generated {txt_output_path}")

def generate_equation_script(department):
    """
    First LLM: Generates {department}_equation.py based on {department}.txt
    """
    txt_path = os.path.join(reports_dir, f"{department}.txt")
    example_eq_path = os.path.join(approche_dir, "example_equation.py")
    output_eq_path = os.path.join(approche_dir, f"{department}_equation.py")
    
    if not os.path.exists(txt_path):
        print(f"Error: {txt_path} not found.")
        return
    
    if not os.path.exists(example_eq_path):
        print("Error: example_equation.py not found.")
        return
    
    report_text = extract_text(txt_path)
    example_eq_code = extract_text(example_eq_path)
    
    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/", 
        temperature=0.5, 
        top_p=0.9)
    instruction = (
        "You are an expert in system dynamics and Python programming. "
        "Your task is to generate a Python script modeling a process using **differential equations**. "
        "Follow the structure from the provided example script."
    )
    
    user_prompt = (
        f"Generate a Python script that models the **{department}** process using system dynamics.\n"
        "**Use differential equations** to represent process flow between different states.\n"
        "Write the system of equations similar to the example provided.\n"
        "**Follow the structure from the provided example script.**\n\n"
        f"Report: {report_text}\n\n"
        "Example equation-based script:\n"
        f"{example_eq_code}\n\n"
        f"Now, generate the Python script exactly similar to the {example_eq_code}, ensure correct variable definitions and equations based on {report_text}.\n\n"
        "Don't write any extra code, just write the equations, variables, and intial values."
    )
    
    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
    with open(output_eq_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Generated {output_eq_path}")

def generate_department_script(department):
    """
    Second LLM: Generates {department}.py based on {department}_equation.py and example.py
    """
    equation_path = os.path.join(approche_dir, f"{department}_equation.py")
    example_path = os.path.join(approche_dir, "example.py")
    example_eq_path = os.path.join(approche_dir, "example_equation.py")
    output_path = os.path.join(approche_dir, f"{department}.py")
    txt_path = os.path.join(reports_dir, f"{department}.txt")
    txt_simulation_path = os.path.join(reports_dir, f"{department}_simulation.txt")
    
    if not os.path.exists(equation_path) or not os.path.exists(example_path):
        print("Error: Required files not found.")
        return
    
    equation_code = extract_text(equation_path)
    example_code = extract_text(example_path)
    example_eq_code = extract_text(example_eq_path)
    report_text = extract_text(txt_path)
    
    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.45,
        top_p=0.9)
    instruction = (
        "You are an expert in Python software engineering. "
        "Your task is to refine and structure a generated system dynamics script. "
        "Ensure the final script follows good coding practices and is executable."
    )
    
    user_prompt = (
        f"Refine and structure a Python script for the **{department}** process.\n"
        "Ensure that it is **executable, efficient, and follows best practices**.\n"
        f"Considering {example_eq_code} leading to {example_code}, generate a python script similar to {example_code}, where you change the equations and variables based on the variables and equations exist in {equation_code}.\n\n"
        "Use object-oriented programming principles where applicable.\n\n"
        f"You may use {report_text} to complete the script.\n\n"
        f"You may use the simulation parameteres mentioned {txt_simulation_path} to add neccessary functions and set the simulation parameters in the script.\n\n"
        # f"Based on {equation_code}, add an additional function to construct a **causal loop diagram** using `networkx`.\n\n"
        # "**Follow the structure of the provided example code to construct a **causal loop diagram** using `networkx`.**\n"
        # "Ensure that:\n"
        # "- Each phase is represented as a **node**\n"
        # "- **Edges** represent the flow between nodes using process rates\n"
        # "- Use `pos = {...}` to correctly align nodes in a visually structured way\n"
        # "- Nodes are well-positioned, labeled, and proportionate to the diagram\n"
        # "- The final diagram clearly represents the system's flow\n\n"
        # "Plot an aligned casual loop diagram, consideirng all the input and out flows, and stocks, with aligned positioned nodes that exactly shows the equations.\n\n"
        "Don't write any extra text."

    )
    
    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Generated {output_path}")


def plot_causal_loop_diagram(department):
    """
    Fourth LLM: Fixes potential errors in {department}.py
    """
    department_script_path = os.path.join(approche_dir, f"{department}.py")
    example_path = os.path.join(approche_dir, "example.py")

    if not os.path.exists(department_script_path):
        print(f"Error: {department_script_path} not found.")
        return
    
    department_code = extract_text(department_script_path)
    example_code = extract_text(example_path)

    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.45, 
        top_p=0.9)
    
    instruction = (
        "You are an expert in python codeing and graphical visulization of python codes of system dynamics. "
        "Your task is to look at a code of a dynamic system and create a graph for it. "
    )
    
    user_prompt = (
        f"Add a function to **{department}.py** to visulize the dynamic processes using `networkx`.\n\n"
        f"Use {example_code} as an example.\n\n"
        "Only return the complete code without extra explanation."
    )


    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
    
    
    with open(department_script_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Graph added {department_script_path}")


def correct_department_script(department):
    """
    Third LLM: Fixes potential errors in {department}.py
    """
    department_script_path = os.path.join(approche_dir, f"{department}.py")
    
    if not os.path.exists(department_script_path):
        print(f"Error: {department_script_path} not found.")
        return
    
    department_code = extract_text(department_script_path)

    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.3, 
        top_p=0.9)
    
    instruction = (
        "You are an expert Python code reviewer. "
        "Your task is to check and correct any errors in the provided script. "
        "Ensure proper function definitions, argument orders, logical correctness, and execution readiness."
    )
    
    user_prompt = (
        f"Review and correct the **{department}.py** script.\n"
        "Fix any **logical errors, argument mismatches, or syntax issues**.\n"
        "Ensure that the script is **fully functional and ready to run**.\n\n"
        "Here is the script that needs correction:\n"
        f"```python\n{department_code}\n```\n\n"
        "Provide the corrected script without any extra text."
    )

    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
    
    # Remove possible Markdown-style code blocks from LLM response
    if result.startswith("```python"):
        result = result[9:]  # Remove the first 9 characters (```python\n)
    if result.endswith("```"):
        result = result[:-3]  # Remove the last 3 characters (```)

    # Strip any leading/trailing spaces or newlines
    result = result.strip()
    
    with open(department_script_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Corrected {department_script_path}")


def run_department_script(department):
    """
    Runs the generated and corrected department script
    """
    script_path = os.path.join(approche_dir, f"{department}.py")
    
    if os.path.exists(script_path):
        print(f"Running {script_path}...\n")
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"Error: {script_path} not found. Unable to run.")

def main():
    department = input("Enter the department name: ").strip()
    generate_simplified_text(department)
    generate_equation_script(department)
    generate_department_script(department)
    plot_causal_loop_diagram(department)
    correct_department_script(department)
    run_department_script(department)

if __name__ == "__main__":
    main()
