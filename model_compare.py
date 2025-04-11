import tkinter as tk
import tkinter.filedialog
from tkinter import *
import pandas as pd
from ratio_functions import mean_absolute_error,mean_square_error,mean_absolute_percentage_error,root_mean_square_error

pd.set_option("display.precision", 10)

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

        data = pd.read_csv(self.file_path, sep=",")
        print(data)
        if self.model_type.get() == 'regresja':
            try:
                true_values = data['rzeczywista']
                model1_preds = data['przewidywana1']
                model2_preds = data['przewidywana2']
                print(model1_preds)
                print(model2_preds)

                MAE_model1 = mean_absolute_error(true_values,model1_preds)
                MSE_model1 = mean_square_error(true_values,model1_preds)
                RMSE_model1 = root_mean_square_error(true_values,model1_preds)
                MAPE_model1 = mean_absolute_percentage_error(true_values,model1_preds)
                print("MAE model1: ",MAE_model1)
                print("MSE model1: ", MSE_model1)
                print("RMSE model1: ", RMSE_model1)
                print("MAPE model1: ", MAPE_model1)

            except NameError:
                raise NameError("Nie znaleziono nazw tabel w data")



