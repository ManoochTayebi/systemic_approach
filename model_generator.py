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
        temperature=0., 
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
        "Don't write any extra code, just write the equations, variables, and intial values."
    )
    
    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
    with open(output_eq_path, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"Generated {output_eq_path}")

# def generate_organization_script(organization):
#     """
#     Second LLM: Generates {organization}.py based on {organization}_equation.py and example.py
#     """
#     equation_path = os.path.join(approche_dir, f"{organization}_equation.py")
#     example_path = os.path.join(approche_dir, "example.py")
#     output_path = os.path.join(approche_dir, f"{organization}.py")
#     txt_path = os.path.join(report_dir, f"{organization}.txt")
#     txt_simulation_path = os.path.join(report_dir, f"{organization}_simulation.txt")
    
#     if not os.path.exists(equation_path) or not os.path.exists(example_path):
#         print("Error: Required files not found.")
#         return
    
#     equation_code = extract_text(equation_path)
#     example_code = extract_text(example_path)
#     report_text = extract_text(txt_path)
    
#     llm = OllamaLLM(
#         model="mistral-small:24b", 
#         base_url="http://smart4lm.llm.solent.fr:11434/",
#         temperature=0.4,
#         top_p=1)
#     instruction = (
#         "You are an expert in Python software engineering. "
#         "Your task is to refine and structure a generated system dynamics script. "
#         "Ensure the final script follows good coding practices and is executable."
#     )
    
#     user_prompt = (
#         f"Use the equation in {equation_code} to develope a script for **{organization}** based on the structure of {example_code}.\n"
#         f"Make sure that similar to the structure of {example_code}, the functions of plot_reults and plot_causal_loop_diagram are well defined based on the variables and equations in {equation_code}.\n"
#         f"You may use {report_text} to complete the script.\n\n"
#         f"You may use the simulation parameteres mentioned {txt_simulation_path} to add neccessary functions and set the simulation parameters in the script.\n\n"
#         "**The script must follow this structure exactly:**\n"
#         "1. **Import Statements**: Include required libraries (e.g., NumPy, SciPy, Matplotlib, NetworkX).\n"
#         f"2. **Class Definition**: Define a class named `{organization}Model` with:\n"
#         "An `__init__` method that initializes process rates, simulation parameters, and system equations.\n"
#         "A method `process_function(self, t, y)` that defines the differential equations modeling the system.\n"
#         "A method `run_simulation(self)` that numerically solves the system of equations using `solve_ivp`.\n"
#         "A method `plot_results(self, sol)` that visualizes simulation results.\n"
#         "A method `plot_causal_loop_diagram(self)` that constructs a directed graph using `networkx`.\n"
#         "3. **Main Execution Block (`if __name__ == '__main__':`)**: Instantiates the model, runs the simulation, and generates visualizations.\n\n"

#         "**Strict constraints for this task:**\n"
#         "- **All function and variable names must match the example script.**\n"
#         f"- **The structure of the class, method definitions, and calls must remain identical to {example_code}.**\n"
#         f"- **Only modify equations and variables according to `{equation_code}`, but do not change the format.**\n"
#         "- **Use OOP principles (e.g., encapsulation in a class).**\n\n"
#         f"Using this template, modify only the equations and parameters based on `{equation_code}` while keeping everything else identical.\n"
#         "Don't write any extra text."
#     )
    
#     result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])
#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(result)
#     print(f"Generated {output_path}")



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




# def generate_organization_solver(organization):
    # """
    # Second LLM: Generates {organization}.py based on {organization}_equation.py and example.py
    # """
    # equation_class_path = os.path.join(approche_dir, f"{organization}_equations_class.py")
    # example_path = os.path.join(example_dir, "example_solver.py")
    # output_path = os.path.join(approche_dir, f"{organization}_solver.py")
    # txt_simulation_path = os.path.join(report_dir, f"{organization}_simulation.txt")
    
    # if not os.path.exists(equation_class_path) or not os.path.exists(example_path):
    #     print("Error: Required files not found.")
    #     return
    
    # equation_code = extract_text(equation_class_path)
    # example_code = extract_text(example_path)
    # txt_simulation = extract_text(txt_simulation_path)
    
    # llm = OllamaLLM(
    #     model="mistral-small:24b", 
    #     base_url="http://smart4lm.llm.solent.fr:11434/",
    #     temperature=0.5,
    #     top_p=1)
    # instruction = (
    #     "You are an expert in Python software engineering. "
    #     "Your task is to generate a script that solves a system of differential equations. "
    #     "Ensure the final script follows good coding practices and is executable."
    # )
    
    # user_prompt = (
    #     f"Generate a script, exactly like the structure of {example_code}, which has only a child class named `{organization}Solver` (child from `{organization}Model` of {equation_code}) with a function of scipy.integrate.solve_ivp to solve the system of equations.\n"
    #     "Don't write any extra text."
    # )
    
    # result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])

    # # Remove possible Markdown-style code blocks from LLM response
    # if result.startswith("```python"):
    #     result = result[9:]  # Remove the first 9 characters (```python\n)
    # if result.endswith("```"):
    #     result = result[:-3]  # Remove the last 3 characters (```)

    # # Strip any leading/trailing spaces or newlines
    # result = result.strip()

    # with open(output_path, "w", encoding="utf-8") as f:
    #     f.write(result)
    # print(f"Generated {output_path}")




def generate_organization_plot(organization):
    """
    Second LLM: Generates {organization}_plot.py based on {organization}_equation.py and example_plot.py
    """
    equation_path = os.path.join(approche_dir, f"{organization}_equation.py")
    example_path = os.path.join(example_dir, "example_plot.py")
    output_path = os.path.join(approche_dir, f"{organization}_plot.py")
    
    if not os.path.exists(equation_path) or not os.path.exists(example_path):
        print("Error: Required files not found.")
        return
    
    equation_code = extract_text(equation_path)
    example_code = extract_text(example_path)
    
    llm = OllamaLLM(
        model="mistral-small:24b", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.2,
        top_p=1)
    instruction = (
        "You are an expert in Python software engineering. "
        "Your task is to write a Python script which can plot the results of the solution of the system of differential equations."
        "Ensure the final script follows good coding practices and is executable."
    )
    
    user_prompt = (
        f"Write a python script similar to the structure of {example_code}, which has a method called PlotResults where the figure title is `{organization} Process Simulation`.\n"
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



def generate_organization_loop(organization):
    """
    Fourth LLM: Generates a causal loop diagram script for {organization}.
    """
    organization_script_path = os.path.join(approche_dir, f"{organization}_equations_class.py")
    example_path = os.path.join(example_dir, "example_loop.py")
    output_path = os.path.join(approche_dir, f"{organization}_loop.py")

    if not os.path.exists(organization_script_path):
        print(f"Error: {organization_script_path} not found.")
        return
    
    organization_code = extract_text(organization_script_path)
    example_code = extract_text(example_path)

    llm = OllamaLLM(
        model="llama3.3:latest", 
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.4, 
        top_p=0.9
    )
    
    instruction = (
        "You are an expert in developing Python scripts for visualizing dynamic systems. "
        "Your task is to analyze a provided system's equations and create a directed graph representing the causal relationships. "
    )
    
    user_prompt = (
        f"Create a Python script named '{organization}_loop.py' that defines a class `PlotCausalLoop` with a method `plot_causal_loop_diagram` "
        "which visualizes a directed graph using NetworkX. The script must adhere to the following:\n"
        "- **Do not redefine the equations from the model** (use the `SibyloneModel` class from the provided script).\n"
        "- **Ensure the class is named `PlotCausalLoop`.**\n"
        "- Extract parameters as nodes from {organization}_equations_class.py.\n"
        "- Extract equations as edges from {organization}_equations_class.py.\n"
        "- Group nodes into three distinct departments and position them closer together compared to nodes from other departments.\n"
        "- Define a dictionary `pos = {...}` where nodes within the same department are positioned together while maintaining an aligned structure.\n"
        "- Only return the full script, without explanations."
    )

    result = llm.invoke([instruction, user_prompt])

    # Remove potential Markdown-style formatting
    if result.startswith("```python"):
        result = result[9:]  
    if result.endswith("```"):
        result = result[:-3]  

    # Strip any extra spaces or newlines
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




def check_and_fix_sibylone_scripts(organization):
    """
    LLM function to verify and fix coherence of all Sibylone scripts:
    - Ensures correct imports across files.
    - Confirms expected class and function definitions.
    - Fixes function signature mismatches.
    - Resolves missing imports or undefined references.
    - Saves corrected versions of the scripts.
    """
    script_paths = {
        "equations": os.path.join(approche_dir, f"{organization}_equations_class.py"),
        "solver": os.path.join(approche_dir, f"{organization}_solver.py"),
        "plot": os.path.join(approche_dir, f"{organization}_plot.py"),
        "loop": os.path.join(approche_dir, f"{organization}_loop.py"),
        "run": os.path.join(approche_dir, f"{organization}_run.py")
    }

    # Ensure all files exist
    for script_name, path in script_paths.items():
        if not os.path.exists(path):
            print(f"Error: {script_name} file not found at {path}")
            return

    # Extract script contents
    scripts = {name: extract_text(path) for name, path in script_paths.items()}

    llm = OllamaLLM(
        model="mistral-small:24b",
        base_url="http://smart4lm.llm.solent.fr:11434/",
        temperature=0.4,
        top_p=1
    )

    instruction = (
        "You are a Python software engineering expert. "
        "Your task is to validate and correct a set of system dynamics scripts to ensure they are fully coherent and functional. "
        "Check that:\n"
        "- Each script imports the correct modules from the other scripts."
        "- All expected classes (`SibyloneModel`, `SibyloneSolver`, `PlotResults`, `PlotCausalLoop`) are defined and properly referenced."
        "- Function signatures across the scripts are consistent."
        "- No missing class methods or incorrect function calls exist."
        "- The scripts can work together without errors when executed."
        "Fix any inconsistencies by modifying the scripts directly."
    )

    user_prompt = (
        f"Here are the contents of the scripts that need to be validated and corrected:\n\n"
        f"--- {organization}_equations_class.py ---\n{scripts['equations']}\n\n"
        f"--- {organization}_solver.py ---\n{scripts['solver']}\n\n"
        f"--- {organization}_plot.py ---\n{scripts['plot']}\n\n"
        f"--- {organization}_loop.py ---\n{scripts['loop']}\n\n"
        f"--- {organization}_run.py ---\n{scripts['run']}\n\n"
        "Please analyze these scripts and return the corrected versions. Ensure all necessary modifications are applied."
    )

    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])

    # Split LLM response into corrected scripts and save them
    corrected_scripts = result.split("--- END ---")  # Assume LLM separates scripts properly
    if len(corrected_scripts) == len(scripts):
        for i, (name, path) in enumerate(script_paths.items()):
            save_text(path, corrected_scripts[i].strip())
            print(f"Updated {path}")
    else:
        print("Error: LLM output does not match expected format.")

    print("All scripts have been checked and corrected.")




def correct_organization_script(organization):
    """
    Third LLM: Fixes potential errors in {organization}.py
    """
    organization_script_path = os.path.join(approche_dir, f"{organization}.py")
    
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
        f"Review and correct the **{organization}.py** script.\n"
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




def main():

    organization = input("Enter the organization name: ").strip()

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
    # generate_organization_equation_class(organization)
    # generate_organization_solver(organization)
    # generate_organization_plot(organization)
    # generate_organization_loop(organization)
    generate_organization_run(organization)
    # correct_organization_script(organization)
    # check_and_fix_sibylone_scripts(organization)
    # run_organization_script(organization)

if __name__ == "__main__":
    main()
