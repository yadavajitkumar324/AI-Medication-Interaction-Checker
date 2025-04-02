import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from core_functions import MedicalInteractionChecker

class MedicalChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Interaction Checker")
        self.root.geometry("800x600")
        
        self.checker = MedicalInteractionChecker()
        
        self.create_widgets()
        self.setup_layout()
    
    def create_widgets(self):
        # Create all GUI widgets
        self.notebook = ttk.Notebook(self.root)
        
        # Interaction Checker Tab
        self.interaction_tab = ttk.Frame(self.notebook)
        self.create_interaction_tab()
        
        # Drug Info Tab
        self.drug_info_tab = ttk.Frame(self.notebook)
        self.create_drug_info_tab()
        
        # Symptom Checker Tab
        self.symptom_tab = ttk.Frame(self.notebook)
        self.create_symptom_tab()
        
        # Add tabs to notebook
        self.notebook.add(self.interaction_tab, text="Interaction Checker")
        self.notebook.add(self.drug_info_tab, text="Drug Information")
        self.notebook.add(self.symptom_tab, text="Symptom Checker")
        
        # Chatbot output area
        self.output_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=15)
        self.output_area.config(state=tk.DISABLED)
        
        # Disclaimer
        self.disclaimer = tk.Label(
            self.root,
            text="Disclaimer: This is for educational purposes only. Always consult a healthcare professional.",
            fg="red",
            wraplength=700
        )
    
    def setup_layout(self):
        # Layout all widgets
        self.notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.output_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.disclaimer.pack(pady=5)
    
    def create_interaction_tab(self):
        # Drug 1
        tk.Label(self.interaction_tab, text="Drug 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.drug1_entry = tk.Entry(self.interaction_tab, width=30)
        self.drug1_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Drug 2
        tk.Label(self.interaction_tab, text="Drug 2:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.drug2_entry = tk.Entry(self.interaction_tab, width=30)
        self.drug2_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Check Button
        check_btn = tk.Button(
            self.interaction_tab,
            text="Check Interaction",
            command=self.check_interaction
        )
        check_btn.grid(row=2, column=0, columnspan=2, pady=10)
    
    def create_drug_info_tab(self):
        # Drug name entry
        tk.Label(self.drug_info_tab, text="Drug Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.drug_info_entry = tk.Entry(self.drug_info_tab, width=30)
        self.drug_info_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Get Info Button
        info_btn = tk.Button(
            self.drug_info_tab,
            text="Get Drug Information",
            command=self.get_drug_info
        )
        info_btn.grid(row=1, column=0, columnspan=2, pady=10)
    
    def create_symptom_tab(self):
        # Symptom entry
        tk.Label(self.symptom_tab, text="Enter Symptom:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.symptom_entry = tk.Entry(self.symptom_tab, width=30)
        self.symptom_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Suggest Button
        suggest_btn = tk.Button(
            self.symptom_tab,
            text="Suggest Medications",
            command=self.suggest_medications  # Changed from suggest_medication to suggest_medications
        )
        suggest_btn.grid(row=1, column=0, columnspan=2, pady=10)
    
    def check_interaction(self):
        drug1 = self.drug1_entry.get().strip()
        drug2 = self.drug2_entry.get().strip()
        
        if not drug1 or not drug2:
            messagebox.showerror("Error", "Please enter both drug names")
            return
        
        drug1_match, drug2_match, result = self.checker.check_interaction(drug1, drug2)
        
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        
        self.output_area.insert(tk.END, f"Checking interaction between:\n")
        self.output_area.insert(tk.END, f"- {drug1} (matched to: {drug1_match if drug1_match else 'unknown'})\n")
        self.output_area.insert(tk.END, f"- {drug2} (matched to: {drug2_match if drug2_match else 'unknown'})\n\n")
        
        if isinstance(result, str):
            self.output_area.insert(tk.END, f"Result: {result}\n")
        else:
            self.output_area.insert(tk.END, "Potential Interactions Found:\n")
            for interaction in result["interactions"]:
                self.output_area.insert(tk.END, f"- {interaction}\n")
            
            self.output_area.insert(tk.END, "\nWarnings:\n")
            for warning in result["warnings"]:
                self.output_area.insert(tk.END, f"- {warning}\n")
        
        self.output_area.config(state=tk.DISABLED)
    
    def get_drug_info(self):
        drug_name = self.drug_info_entry.get().strip()
        
        if not drug_name:
            messagebox.showerror("Error", "Please enter a drug name")
            return
        
        drug_match, info = self.checker.get_drug_info(drug_name)
        
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        
        self.output_area.insert(tk.END, f"Information for: {drug_name}\n")
        self.output_area.insert(tk.END, f"Matched to: {drug_match if drug_match else 'unknown'}\n\n")
        
        if isinstance(info, str):
            self.output_area.insert(tk.END, info + "\n")
        else:
            self.output_area.insert(tk.END, f"Drug Type: {info.get('type', 'Unknown')}\n")
            self.output_area.insert(tk.END, f"Known Interactions: {', '.join(info.get('interactions', []))}\n")
            self.output_area.insert(tk.END, f"Warnings: {info.get('warnings', 'None')}\n")
        
        self.output_area.config(state=tk.DISABLED)
    
    def suggest_medications(self):  # Changed from suggest_medication to suggest_medications
        symptom = self.symptom_entry.get().strip()
        
        if not symptom:
            messagebox.showerror("Error", "Please enter a symptom")
            return
        
        matched_symptom, suggestions = self.checker.suggest_medication(symptom)
        
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)
        
        self.output_area.insert(tk.END, f"Medication suggestions for: {symptom}\n")
        self.output_area.insert(tk.END, f"Matched to symptom: {matched_symptom}\n\n")
        
        if isinstance(suggestions, str):
            self.output_area.insert(tk.END, suggestions + "\n")
        else:
            self.output_area.insert(tk.END, "Possible medications:\n")
            for med in suggestions:
                self.output_area.insert(tk.END, f"\n- {med['name']} ({med['type']})\n")
                self.output_area.insert(tk.END, f"  Warnings: {med['warnings']}\n")
        
        self.output_area.config(state=tk.DISABLED)