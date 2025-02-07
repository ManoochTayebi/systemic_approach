import os
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage

# Define directories
base_dir = os.getcwd()  # Get current working directory
reports_dir = os.path.join(base_dir, "reports")  # Folder containing text reports
output_dir = os.path.join(base_dir, "approche_systemique")  # Folder for generated Python scripts

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def generate_python_script(department):
    """
    Generate a Python script that models the department process using system dynamics.

    Args:
        department (str): The name of the department.
    """

    # Define file paths
    txt_path = os.path.join(reports_dir, f"{department}.txt")  # Department report
    example_path = os.path.join(output_dir, "example.py")  # Reference example script
    output_path = os.path.join(output_dir, f"{department}.py")  # Output Python script

    # Check if the text file exists
    if not os.path.exists(txt_path):
        print(f"Error: The file '{txt_path}' does not exist. Please check the department name.")
        return

    # Check if the example file exists
    if not os.path.exists(example_path):
        print(f"Error: The reference file 'example.py' does not exist. Ensure it's in the folder.")
        return

    # Function to extract text from a text file
    def extract_text_from_txt(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    # Read the report
    report_text = extract_text_from_txt(txt_path)

    # Read the example script to maintain structure
    example_code = extract_text_from_txt(example_path)

    # Configure the LLM
    local_llm = "llama3.3:latest"
    base_url = "http://smart4lm.llm.solent.fr:11434/"
    llm = OllamaLLM(
        model=local_llm,
        base_url=base_url,
        temperature=0.5,
        top_p=0.9
    )

    # System instruction
    instruction = (
        "You are an expert in system dynamics modeling and Python programming. "
        "Your task is to generate a Python script that models a process using **differential equations**. "
        "The equations must represent the flow between different states of the system. "
        "Use **NumPy and SciPy** for computation and **Matplotlib** for visualization. "
        "Ensure the model is well-structured, with comments explaining key parts. "
        "Follow the structure from the provided example script."
    )

    # User prompt
    user_prompt = (
        f"Generate a Python script that models the **{department}** process using system dynamics.\n"
        "**Use differential equations** to represent process flow between different states.\n"
        "**Follow the structure from the provided example script.**\n\n"
        f"Here is the report of a dynamic organization (Business department) from the text file:\n{report_text}\n\n"
        " The dynamic organization has different phases and at each phase it has some inputes and some outputs.\n\n"
        "You may write a python code to model the behavior of this dynamic organization with partial differntial equations as in the following we have an example of another dynamic system as a template:\n\n"
        f"{example_code}\n\n"
        "Now, generate the Python script.\n\n"
        "Define classes and functions in the code.\n\n"
        "You may choose name of the variables corresponding to the variables in the report file.\n\n" 
        "Use the variables and parameters based on the values mentioned in the report.\n\n"
        "Make sure all the variables and equations are correctly defined and the code is executable.\n\n"
        "If you can't find a variable, form the txt file and it is missing for the equations, you may use a random but conservative value for it.\n\n"
        "Just write the python script and don't add any extra text to it.\n\n"
        # "Make sure that the input of the function system_of_equations(self, t, state) having the right order of the variables so that solve_ivp can run properly."
    )

    # Invoke LLM
    result = llm.invoke([SystemMessage(content=instruction), HumanMessage(content=user_prompt)])

    # Save the result to a Python file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Python script saved as {output_path}")

def main():
    department = input("Enter the department name: ").strip()
    generate_python_script(department)

if __name__ == "__main__":
    main()
