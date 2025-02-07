import os
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
        # "Use NumPy and SciPy for computation and Matplotlib for visualization. "
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
        "Don't write any exrta code, just write the equations and variables."

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
    
    if not os.path.exists(equation_path) or not os.path.exists(example_path):
        print("Error: Required files not found.")
        return
    
    equation_code = extract_text(equation_path)
    example_code = extract_text(example_path)
    example_eq_code = extract_text(example_eq_path)
    
    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.5,
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
        "Don't write any extra text."
    )
    
    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Generated {output_path}")

def main():
    department = input("Enter the department name: ").strip()
    generate_equation_script(department)
    generate_department_script(department)

if __name__ == "__main__":
    main()
