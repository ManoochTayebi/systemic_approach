import os
import sys
import subprocess
import docx
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage

# Define directories
base_dir = os.getcwd()
report_dir = os.path.join(base_dir, "report")
example_dir = os.path.join(base_dir, "structure")
approche_dir = os.path.join(base_dir, "approche_systemique")

# Ensure output directory exists
os.makedirs(approche_dir, exist_ok=True)
os.makedirs(example_dir, exist_ok=True)

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
    
def process_report(department):
    """Processes report only for a given department."""
    extracted_texts = []
    
    for file_name in os.listdir(report_dir):
        if not file_name.lower().startswith(department.lower()):  # Filter department reports
            continue

        file_path = os.path.join(report_dir, file_name)
        extracted_text = ""

        if file_name.endswith(".txt"):
            extracted_text = extract_text(file_path)
        elif file_name.endswith(".docx"):
            extracted_text = extract_text_from_docx(file_path)

        if extracted_text:
            extracted_texts.append(f"{extracted_text}\n")
    
    return "\n".join(extracted_texts) if extracted_texts else None


def generate_equation_script(organization):
    """
    First LLM: Generates {organization}_equation.py based on {organization}.txt
    """
    txt_path = os.path.join(report_dir, f"{organization}.txt")
    example_eq_path = os.path.join(example_dir, "example_equation.py")
    output_eq_path = os.path.join(approche_dir, f"{organization}_equation.py")
    
    if not os.path.exists(txt_path):
        print(f"Error: {txt_path} not found.")
        return
    
    if not os.path.exists(example_eq_path):
        print("Error: example_equation.py not found.")
        return
    
    report_text = extract_text(txt_path)
    example_eq_code = extract_text(example_eq_path)
    
    llm = OllamaLLM(
        model="llama3.3:latest",       # MMT202402020: This model is a good model to generate the dynamic equations.
        base_url="http://smart4lm.llm.solent.fr:11434/", 
        temperature=0.2, 
        top_p=0.9)
    instruction = (
        "You are an expert in system dynamics and Python programming. "
        "Your task is to generate a Python script modeling a process using **differential equations**. "
        "Follow the structure from the provided example script."
    )
    
    user_prompt = (
        f"Generate a Python script that models the **{organization}** process using system dynamics.\n"
        "Write the **differential equations** to represent process flow between different states.\n"
        f"Write the system of equations similar to the structure of {example_eq_code}, ensuring correct variable definitions and equations based on {report_text}.\n\n"
        "Use complete variable names in the equations.\n"
        "Don't write any extra code, just write the equations, variables, and intial values."
    )
    
    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
    with open(output_eq_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Generated {output_eq_path}")



def generate_organization_equation_class(organization):
    """
    Second LLM: Generates {organization}.py based on {organization}_equation.py and example.py
    """
    equation_path = os.path.join(approche_dir, f"{organization}_equation.py")
    example_path = os.path.join(example_dir, "example_equations_class.py")
    output_path = os.path.join(approche_dir, f"{organization}_equations_class.py")
    txt_path = os.path.join(report_dir, f"{organization}.txt")
    txt_simulation_path = os.path.join(report_dir, f"{organization}_simulation.txt")
    
    if not os.path.exists(equation_path) or not os.path.exists(example_path):
        print("Error: Required files not found.")
        return
    
    equation_code = extract_text(equation_path)
    example_code = extract_text(example_path)
    report_text = extract_text(txt_path)
    txt_simulation = extract_text(txt_simulation_path)
    
    llm = OllamaLLM(
        model="mistral-small:24b", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.1,
        top_p=1)
    instruction = (
        "You are an expert in Python software engineering. "
        "Your task is to refine and structure a generated system dynamics script. "
        "Ensure the final script follows good coding practices and is executable."
    )
    
    user_prompt = (
        f"Use the equation in {equation_code} to develope a script for **{organization}** based on the structure of {example_code}.\n"
        f"Create a class similar to the structure of {example_code}, based on the variables and equations in {equation_code}.\n"
        f"You may use {report_text} to complete the script.\n\n"
        f"You may use the simulation parameteres mentioned {txt_simulation} to add neccessary functions and set the simulation parameters in the script.\n\n"
        f"**Class Definition**: Define a class named `{organization}Model` with:\n"
        f"Using this template, modify only the equations and parameters based on `{equation_code}` while keeping everything else identical.\n"
        "Make sure that you store the varirables name and add a function called `get_variable_names` that returns the list of variable names.\n"
        "Don't write the example usage, I just want the functions without it being an executable script by itself."
        "Don't write any extra text."
    )
    
    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])

    # Remove possible Markdown-style code blocks from LLM response
    if result.startswith("```python"):
        result = result[9:]  # Remove the first 9 characters (```python\n)
    if result.endswith("```"):
        result = result[:-3]  # Remove the last 3 characters (```)

    # Strip any leading/trailing spaces or newlines
    result = result.strip()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Generated {output_path}")



def generate_organization_run(organization):
    """
    Second LLM: Generates {organization}_run.py based on {organization}_equations_class.py,
    {organization}_solver.py, {organization}_plot.py, {organization}_loop.py, and example_run.py.
    """
    equation_path = os.path.join(approche_dir, f"{organization}_equations_class.py")
    example_path = os.path.join(example_dir, "example_run.py")
    output_path = os.path.join(approche_dir, f"{organization}_run.py")

    # Check if all required files exist
    for path in [equation_path, example_path]:
        if not os.path.exists(path):
            print(f"Error: {path} not found.")
            return

    # Extract content from each relevant file
    equation_code = extract_text(equation_path)
    example_code = extract_text(example_path)

    llm = OllamaLLM(
        model="mistral-small:24b",
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.4,
        top_p=1
    )

    instruction = (
        "You are an expert in Python software engineering. "
        "Your task is to generate a clean and executable Python script that follows best practices. "
        "The script should use the following modules to run a system dynamics simulation:\n"
        f"- {equation_code} (contains model equations)\n"
        "Ensure the generated script mirrors the structure of `example_run.py` while using the Sibylone components."
    )

    user_prompt = (
        f"Write a script similar to the structure of {example_code} that run the simulation of the system dynamics based on {equation_path} and plot the graphs.\n"
        "Only return the full Python script without extra explanation."
    )


    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])

    # Remove potential Markdown formatting issues from LLM response
    if result.startswith("```python"):
        result = result[9:]  # Remove first 9 characters (```python\n)
    if result.endswith("```"):
        result = result[:-3]  # Remove last 3 characters (```)

    # Strip any leading/trailing spaces or newlines
    result = result.strip()

    # Write the generated script to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Generated {output_path}")


def correct_organization_script(organization):
    """
    Third LLM: Fixes potential errors in {organization}.py
    """
    organization_script_path = os.path.join(approche_dir, f"{organization}_equations_class.py")
    
    if not os.path.exists(organization_script_path):
        print(f"Error: {organization_script_path} not found.")
        return
    
    organization_code = extract_text(organization_script_path)

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
        f"Review and correct the **{organization}_equaitons_class.py** script.\n"
        "Fix any **logical errors, argument mismatches, or syntax issues**.\n"
        "Ensure that the script is **fully functional and ready to run**.\n\n"
        "Here is the script that needs correction:\n"
        f"```python\n{organization_code}\n```\n\n"
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
    
    with open(organization_script_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Corrected {organization_script_path}")



def correct_run_script(organization):
    """
    Third LLM: Fixes potential errors in {organization}.py
    """
    organization_script_path = os.path.join(approche_dir, f"{organization}_equations_class.py")
    organization_run_path = os.path.join(approche_dir, f"{organization}_run.py")
    
    if not os.path.exists(organization_run_path):
        print(f"Error: {organization_run_path} not found.")
        return
    
    organization_code = extract_text(organization_script_path)
    organization_run = extract_text(organization_run_path)

    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.3, 
        top_p=0.9)
    
    instruction = (
        "You are an expert Python code reviewer."
        "Your task is to check and correct any errors in the provided script. "
        "Ensure proper function definitions, argument orders, logical correctness, and execution readiness."
    )
    
    user_prompt = (
        f"Review and correct the {organization_run} script.\n"
        "Fix any **logical errors, argument mismatches, or syntax issues**.\n"
        "Ensure that the script is **fully functional and ready to run**.\n\n"
        f"Make sure that it is adapted to {organization_code}.\n\n"
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
    
    with open(organization_run_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Corrected {organization_run_path}")




def adapt_run_script(organization):
    """
    Third LLM: Fixes potential errors in {organization}.py
    """
    organization_script_path = os.path.join(approche_dir, f"{organization}_equations_class.py")
    organization_run_path = os.path.join(approche_dir, f"{organization}_run.py")
    simulation_txt_path = os.path.join(report_dir, f"{organization}_simulation.txt")
    
    if not os.path.exists(organization_run_path):
        print(f"Error: {organization_run_path} not found.")
        return
    
    organization_code = extract_text(organization_script_path)
    organization_run = extract_text(organization_run_path)
    simulation_txt = extract_text(simulation_txt_path)

    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.3, 
        top_p=0.9)
    
    instruction = (
        "You are an expert Python code reviewer."
        "Your task is to check a python script and adpat it to a new simulation parameters from a text. "
        "Ensure proper function definitions, argument orders, logical correctness, and execution readiness."
    )
    
    user_prompt = (
        f"Review the {organization_run} script and use simulation time to the simulation parameter in {simulation_txt}.\n"
        f"Review the {organization_run} script and adapt the plot function so that it only plots the variables mentioned in {simulation_txt}.\n"
        f"Make sure that it is adapted to {organization_code}.\n\n"
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
    
    with open(organization_run_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Adapted {organization_run_path}")



def plot_causal_loop_diagram(organization):
    """
    Fourth LLM: Fixes potential errors in {department}.py
    """
    organization_loop_path = os.path.join(approche_dir, f"{organization}_loop.py")
    example_loop_path = os.path.join(example_dir, "example_loop.py")
    txt_path = os.path.join(report_dir, f"{organization}.txt")
    

    if not os.path.exists(example_loop_path):
        print(f"Error: {example_loop_path} not found.")
        return
    
    # organization_loop = extract_text(organization_loop_path)
    example_loop = extract_text(example_loop_path)
    report_txt = extract_text(txt_path)

    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.45, 
        top_p=0.9)
    
    instruction = (
        "You are an expert in python codeing and graphical visulization of python codes of system dynamics. "
        "Your task is to look at the report of a dynamic system and create a graph for it. "
    )
    
    user_prompt = (
        f"Generate a script similar to the structure of {example_loop} which generates a causal loop diagram for the basde on {report_txt}.\n"
        "Make sure the code is correct and executable.\n"
        "Only return the complete code without extra explanation."
    )


    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
    
    # Remove potential Markdown formatting issues from LLM response
    if result.startswith("```python"):
        result = result[9:]  # Remove first 9 characters (```python\n)
    if result.endswith("```"):
        result = result[:-3]  # Remove last 3 characters (```)

    # Strip any leading/trailing spaces or newlines
    result = result.strip()

    with open(organization_loop_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Graph added {organization_loop_path}")




def run_organization_script(organization):
    """
    Runs the generated and corrected organization script
    """
    script_path = os.path.join(approche_dir, f"{organization}_run.py")
    
    if os.path.exists(script_path):
        print(f"Running {script_path}...\n")
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"Error: {script_path} not found. Unable to run.")


def run_organization_loop(organization):
    """
    Runs the generated and corrected organization script
    """
    script_path = os.path.join(approche_dir, f"{organization}_loop.py")
    
    if os.path.exists(script_path):
        print(f"Running {script_path}...\n")
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"Error: {script_path} not found. Unable to run.")


def correct_organization_loop(organization):
    """
    Third LLM: Fixes potential errors in {organization}.py
    """
    organization_script_path = os.path.join(approche_dir, f"{organization}_loop.py")
    
    if not os.path.exists(organization_script_path):
        print(f"Error: {organization_script_path} not found.")
        return
    
    organization_code = extract_text(organization_script_path)

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
        f"Review and correct the **{organization}_loop.py** script.\n"
        "Fix any **logical errors, argument mismatches, or syntax issues**.\n"
        "Ensure that the script is **fully functional and ready to run**.\n\n"
        "Here is the script that needs correction:\n"
        f"```python\n{organization_code}\n```\n\n"
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
    
    with open(organization_script_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    print(f"Corrected {organization_script_path}")

def main():

    # organization = input("Enter the organization name: ").strip()
    organization = "Sibylone"

    # all_reports = []
    
    # while True:
    #     department = input("Enter the department name (or press Enter to finish): ").strip()
    #     if not department:
    #         break

    #     department_text = process_report(department)
    #     if department_text:
    #         all_reports.append(f"===== {department.upper()} REPORTS =====\n{department_text}\n")
    #     else:
    #         print(f"No reports found for {department}.")
    
    # if all_reports:
    #     final_report_path = os.path.join(report_dir, f"{organization}.txt")
    #     with open(final_report_path, "w", encoding="utf-8") as final_file:
    #         final_file.write("\n".join(all_reports))
    #     print(f"Consolidated report saved at: {final_report_path}")
    # else:
    #     print("No reports were processed.")

    # generate_equation_script(organization)
    generate_organization_equation_class(organization)
    generate_organization_run(organization)
    correct_organization_script(organization)
    adapt_run_script(organization)
    correct_run_script(organization)
    # plot_causal_loop_diagram(organization)
    # correct_organization_loop(organization)
    run_organization_script(organization)
    run_organization_loop(organization)

if __name__ == "__main__":
    main()
