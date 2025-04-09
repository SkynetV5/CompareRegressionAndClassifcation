import tkinter as tk
import tkinter.filedialog
from tkinter import *

class ModelCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Porównianie modeli regresji / klasyfikacji")

        self.file_path = None
        self.model_type = tk.StringVar(value="regresja")

        self.load_button = tk.Button(root,text="Wczytaj plik CSV", command=self.load_file)
        self.load_button.pack(pady=10)

        self.file_label = tk.Label(root, text="Nie wybrano pliku", wraplength=300, justify="center")
        self.file_label.pack()

        self.model_frame = tk.Frame(root)
        self.model_frame.pack(pady=10)

        tk.Label(self.model_frame, text="Wybierz typ modelu:").pack(anchor="w")

        self.radio_regression = tk.Radiobutton(self.model_frame, text="Regresja",variable=self.model_type, value="regresja")
        self.radio_classification = tk.Radiobutton(self.model_frame,text="Klasyfikacja", variable=self.model_type, value="klasyfikacja")
        self.radio_regression.pack(anchor="w")
        self.radio_classification.pack(anchor="w")

        self.analyze_button = tk.Button(root,text="Analizuj", state=tk.DISABLED, command=self.analyze)
        self.analyze_button.pack(pady=10)

    def load_file(self):
        file_types = [("CSV files", "*.csv")]
        path = tkinter.filedialog.askopenfilename(title="Wybierz plik csv:", filetypes=file_types)
        if path:
            self.file_path = path
            self.file_label.config(text=f"Wybrano plik:\n{path.split('/')[-1]}")
        self.check_read()

    def check_read(self):
        if self.file_path and self.model_type.get():
            self.analyze_button.config(state=tk.NORMAL)
        else:
            self.analyze_button.config(state=tk.DISABLED)

    def analyze(self):
        pass
