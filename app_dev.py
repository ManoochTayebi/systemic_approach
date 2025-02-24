import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, 
    QLineEdit, QFileDialog, QScrollArea, QFormLayout, QTextEdit, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from model_generator import (
    process_report, generate_equation_script, generate_organization_equation_class,
    generate_organization_run, correct_organization_script, adapt_run_script,
    correct_run_script, plot_causal_loop_diagram, correct_organization_loop,
    run_organization_script, run_organization_loop
)

class OrganizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organization Simulation")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("background-color: #f4f4f4; font-family: Arial;")

        self.departments = []
        
        self.org_name_input = QLineEdit(self)
        self.org_name_input.setPlaceholderText("Enter Organization Name")
        self.org_name_input.setStyleSheet("padding: 5px; font-size: 14px;")
        
        self.add_department_btn = QPushButton("Add Department", self)
        self.run_simulation_btn = QPushButton("Run Simulation", self)
        
        for btn in [self.add_department_btn, self.run_simulation_btn]:
            btn.setStyleSheet("background-color: #0078D7; color: white; padding: 8px; font-size: 14px; border-radius: 5px;")
        
        self.simulation_duration_input = QLineEdit(self)
        self.simulation_duration_input.setPlaceholderText("Enter duration (weeks)")
        self.simulation_duration_input.setStyleSheet("padding: 5px; font-size: 14px;")
        
        self.state_variable_inputs = []
        self.state_variable_layout = QVBoxLayout()
        self.add_state_variable_btn = QPushButton("Add State Variable")
        self.add_state_variable_btn.setStyleSheet("background-color: #28a745; color: white; padding: 6px; border-radius: 5px;")
        self.add_state_variable_btn.clicked.connect(self.add_state_variable)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Organization Name:"))
        self.layout.addWidget(self.org_name_input)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_department_btn)
        button_layout.addWidget(self.run_simulation_btn)
        self.layout.addLayout(button_layout)
        
        self.layout.addWidget(QLabel("Simulation Duration (weeks):"))
        self.layout.addWidget(self.simulation_duration_input)
        
        self.layout.addWidget(QLabel("State Variables to Plot:"))
        self.layout.addLayout(self.state_variable_layout)
        self.layout.addWidget(self.add_state_variable_btn)
        
        self.scroll_area = QScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: 1px solid #ccc; background: white; padding: 5px;")
        
        self.layout.addWidget(self.scroll_area)
        self.figures_widget = QWidget()
        self.figures_layout = QVBoxLayout()
        self.figures_widget.setLayout(self.figures_layout)
        self.layout.addWidget(self.figures_widget)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.add_department_btn.clicked.connect(self.add_department)
        self.run_simulation_btn.clicked.connect(self.run_simulation)
    
    def add_department(self):
        department_name = QLineEdit(self)
        department_name.setPlaceholderText("Enter Department Name")
        file_upload_btn = QPushButton("Upload Report", self)
        file_label = QLabel("No file selected", self)
        
        file_upload_btn.setStyleSheet("background-color: #28a745; color: white; padding: 6px; border-radius: 5px;")
        
        def upload_file():
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Report", "", "Text Files (*.txt)")
            if file_path:
                file_label.setText(os.path.basename(file_path))
                self.departments.append((department_name.text(), file_path))
        
        file_upload_btn.clicked.connect(upload_file)
        
        dept_layout = QFormLayout()
        dept_layout.addRow("Department Name:", department_name)
        dept_layout.addRow(file_upload_btn, file_label)
        
        dept_widget = QWidget()
        dept_widget.setLayout(dept_layout)
        dept_widget.setStyleSheet("border: 1px solid #ddd; padding: 10px; margin: 5px; background: white;")
        
        self.scroll_layout.addWidget(dept_widget)
    
    def add_state_variable(self):
        state_variable_input = QLineEdit(self)
        state_variable_input.setPlaceholderText("Enter state variable")
        state_variable_input.setStyleSheet("padding: 5px; font-size: 14px;")
        self.state_variable_inputs.append(state_variable_input)
        self.state_variable_layout.addWidget(state_variable_input)
    
    def run_simulation(self):
        org_name = self.org_name_input.text()
        duration = self.simulation_duration_input.text()
        state_variables = [var.text() for var in self.state_variable_inputs if var.text()]
        
        if not org_name or not duration or not state_variables:
            QMessageBox.warning(self, "Error", "Please provide all required information.")
            return
        
        report_dir = os.path.join(os.getcwd(), "report")
        os.makedirs(report_dir, exist_ok=True)
        simulation_file_path = os.path.join(report_dir, f"{org_name}_simulation.txt")
        
        with open(simulation_file_path, "w") as file:
            file.write(f"Simulation parameters:\n- Run the simulation for {duration} time units (weeks)\n\n")
            file.write("Visualization parameters:\n")
            for var in state_variables:
                file.write(f"- Plot the number of ({var}).\n")
        
        print(f"Simulation parameters saved in {simulation_file_path}")
        
        # generate_equation_script(org_name)
        # generate_organization_equation_class(org_name)
        # generate_organization_run(org_name)
        # correct_organization_script(org_name)
        # adapt_run_script(org_name)
        # correct_run_script(org_name)
        # plot_causal_loop_diagram(org_name)
        # correct_organization_loop(org_name)
        
        run_organization_script(org_name)
        run_organization_loop(org_name)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrganizationApp()
    window.show()
    sys.exit(app.exec_())