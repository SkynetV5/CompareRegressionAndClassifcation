import tkinter as tk
from tkinter import *

class ModelCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Porównianie modeli regresji / klasyfikacji")

        self.file_path = None
        self.model_type = tk.StringVar(value="regresja")

        self.load_button = tk.Button(root,text="Wczytaj plik CSV")
        self.load_button.pack(pady=10)

        self.file_label = tk.Label(root, text="Nie wybrano pliku")
        self.file_label.pack()

        self.model_frame = tk.Frame(root)
        self.model_frame.pack(pady=10)

        tk.Label(self.model_frame, text="Wybierz typ modelu:").pack(anchor="w")

        self.radio_regression = tk.Radiobutton(self.model_frame, text="Regresja",variable=self.model_type, value="regresja")
        self.radio_classification = tk.Radiobutton(self.model_frame,text="Klasyfikacja", variable=self.model_type, value="klasyfikacja")
        self.radio_regression.pack(anchor="w")
        self.radio_classification.pack(anchor="w")

        self.analyze_button = tk.Button(root,text="Analizuj", state=tk.DISABLED)
        self.analyze_button.pack(pady=10)

