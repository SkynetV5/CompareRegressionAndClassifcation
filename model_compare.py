import tkinter as tk
import tkinter.filedialog
from tkinter import *
import pandas as pd
from ratio_functions import mean_absolute_error,mean_square_error,mean_absolute_percentage_error,root_mean_square_error
from draw_charts import draw_histogram
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
      
        if self.model_type.get() == 'regresja':
            try:
                true_values = data['rzeczywista']
                model1_preds = data['przewidywana1']
                model2_preds = data['przewidywana2']

                true_values = [float(x) for x in true_values]
                model1_preds = [float(x) for x in model1_preds]
                model2_preds = [float(x) for x in model2_preds]


                MAE_model1 = mean_absolute_error(true_values,model1_preds)
                MSE_model1 = mean_square_error(true_values,model1_preds)
                RMSE_model1 = root_mean_square_error(true_values,model1_preds)
                MAPE_model1 = mean_absolute_percentage_error(true_values,model1_preds)

                MAE_model2 = mean_absolute_error(true_values, model2_preds)
                MSE_model2 = mean_square_error(true_values, model2_preds)
                RMSE_model2 = root_mean_square_error(true_values, model2_preds)
                MAPE_model2 = mean_absolute_percentage_error(true_values, model2_preds)

                results_window = Toplevel(self.root)  # Tworzymy nowe okno
                app_results = ModelResultsApp(results_window)
                app_results.display_results_regression(MAE_model1, MSE_model1, RMSE_model1, MAPE_model1,
                                            MAE_model2, MSE_model2, RMSE_model2, MAPE_model2, true_values,
                                            model1_preds,model2_preds)
            except NameError:
                raise NameError("Nie znaleziono nazw tabel w data")

        elif self.model_type.get() == 'klasyfikacja':
            pass



class ModelResultsApp:
    def __init__(self,root):
        self.root = root
        self.root.title = "Wyniki analizy:"

        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(pady=10)

        self.model1_mae = tk.LabelFrame(self.results_frame, text="Model 1", padx=10, pady=10)
        self.model1_mae.pack(side="left", padx=10)

        self.model2_mae = tk.LabelFrame(self.results_frame, text="Model 2", padx=10, pady=10)
        self.model2_mae.pack(side="left", padx=10)


        self.chart_container = tk.Frame(self.root)
        self.chart_container.pack(pady=10)

        self.chart_frame_model1 = tk.Frame(self.chart_container)
        self.chart_frame_model1.pack(side="left", padx=10)

        self.chart_frame_model2 = tk.Frame(self.chart_container)
        self.chart_frame_model2.pack(side="left", padx=10)

    def display_results_regression(self, MAE_model1, MSE_model1, RMSE_model1, MAPE_model1,
                        MAE_model2, MSE_model2, RMSE_model2, MAPE_model2, true_values, model1_preds,model2_preds):

        better_model_font = ("Helvetica", 12, "bold")
        normal_font = ("Helvetica", 12)

        tk.Label(self.model1_mae, text=f"MAE: {MAE_model1:.2f}",
                 font=better_model_font if MAE_model1 < MAE_model2 else normal_font).pack(anchor="center")
        tk.Label(self.model1_mae, text=f"MSE: {MSE_model1:.2f}",
                 font=better_model_font if MSE_model1 < MSE_model2 else normal_font).pack(anchor="center")
        tk.Label(self.model1_mae, text=f"RMSE: {RMSE_model1:.2f}",
                 font=better_model_font if RMSE_model1 < RMSE_model2 else normal_font).pack(anchor="center")
        tk.Label(self.model1_mae, text=f"MAPE: {MAPE_model1:.2f}",
                 font=better_model_font if MAPE_model1 < MAPE_model2 else normal_font).pack(anchor="center")

        tk.Label(self.model2_mae, text=f"MAE: {MAE_model2:.2f}",
                 font=better_model_font if MAE_model1 > MAE_model2 else normal_font).pack(anchor="center")
        tk.Label(self.model2_mae, text=f"MSE: {MSE_model2:.2f}",
                 font=better_model_font if MSE_model1 > MSE_model2 else normal_font).pack(anchor="center")
        tk.Label(self.model2_mae, text=f"RMSE: {RMSE_model2:.2f}",
                 font=better_model_font if RMSE_model1 > RMSE_model2 else normal_font).pack(anchor="center")
        tk.Label(self.model2_mae, text=f"MAPE: {MAPE_model2:.2f}",
                 font=better_model_font if MAPE_model1 > MAPE_model2 else normal_font).pack(anchor="center")

        draw_histogram(true_values, model1_preds, "Model1", self.chart_frame_model1)
        draw_histogram(true_values, model2_preds, "Model2", self.chart_frame_model2)




