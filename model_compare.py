import tkinter as tk
import tkinter.filedialog
from tkinter import *
import pandas as pd
from ratio_functions import (
    mean_absolute_error,
    mean_square_error,
    mean_absolute_percentage_error,
    root_mean_square_error,
    accuracy,
    specifity,
    overall_error_rate,
    precision,
    f1_score,
    sensivity,
    false_negative_rate,
    false_positive_rate,
    false_negative_propotion,
    false_positive_propotion,
    true_negative_propotion,
)
from draw_charts import draw_histogram, draw_curve_ROC

pd.set_option("display.precision", 10)


class ModelCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Porównianie modeli regresji / klasyfikacji")

        self.file_path = None
        self.model_type = tk.StringVar(value="regresja")

        self.load_button = tk.Button(
            root, text="Wczytaj plik CSV", command=self.load_file
        )
        self.load_button.pack(pady=10)

        self.file_label = tk.Label(
            root, text="Nie wybrano pliku", wraplength=300, justify="center"
        )
        self.file_label.pack()

        self.model_frame = tk.Frame(root)
        self.model_frame.pack(pady=10)

        tk.Label(self.model_frame, text="Wybierz typ modelu:").pack(anchor="w")

        self.radio_regression = tk.Radiobutton(
            self.model_frame,
            text="Regresja",
            variable=self.model_type,
            value="regresja",
        )
        self.radio_classification = tk.Radiobutton(
            self.model_frame,
            text="Klasyfikacja",
            variable=self.model_type,
            value="klasyfikacja",
        )
        self.radio_regression.pack(anchor="w")
        self.radio_classification.pack(anchor="w")

        self.analyze_button = tk.Button(
            root, text="Analizuj", state=tk.DISABLED, command=self.analyze
        )
        self.analyze_button.pack(pady=10)

    def load_file(self):
        file_types = [("CSV files", "*.csv")]
        path = tkinter.filedialog.askopenfilename(
            title="Wybierz plik csv:", filetypes=file_types
        )
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

        if self.model_type.get() == "regresja":
            try:
                true_values = data.iloc[:, 0]
                model1_preds = data.iloc[:, 1]
                model2_preds = data.iloc[:, 2]

                true_values = [float(x) for x in true_values]
                model1_preds = [float(x) for x in model1_preds]
                model2_preds = [float(x) for x in model2_preds]

                MAE_model1 = mean_absolute_error(true_values, model1_preds)
                MSE_model1 = mean_square_error(true_values, model1_preds)
                RMSE_model1 = root_mean_square_error(true_values, model1_preds)
                MAPE_model1 = mean_absolute_percentage_error(true_values, model1_preds)

                MAE_model2 = mean_absolute_error(true_values, model2_preds)
                MSE_model2 = mean_square_error(true_values, model2_preds)
                RMSE_model2 = root_mean_square_error(true_values, model2_preds)
                MAPE_model2 = mean_absolute_percentage_error(true_values, model2_preds)

                regression_models = {}

                regression_models["MAE"] = [MAE_model1, MAE_model2]
                regression_models["MSE"] = [MSE_model1, MSE_model2]
                regression_models["RMSE"] = [RMSE_model1, RMSE_model2]
                regression_models["MAPE"] = [MAPE_model1, MAPE_model2]

                results_window = Toplevel(self.root)
                results_window.title("Wyniki analizy regresji")
                app_results = ModelResultsApp(results_window)
                app_results.display_results_regression(
                    regression_models,
                    true_values,
                    model1_preds,
                    model2_preds,
                )

            except Exception:
                raise Exception("Błąd!")

        elif self.model_type.get() == "klasyfikacja":
            try:
                true_values = data.iloc[:, 0]
                model1_preds = data.iloc[:, 1]
                model1_prob = data.iloc[:, 2]
                model2_preds = data.iloc[:, 3]
                model2_prob = data.iloc[:, 4]

                conf_matrix_model_1 = pd.crosstab(
                    true_values,
                    model1_preds,
                    rownames=["Rzeczywista"],
                    colnames=["Przewidywana"],
                )

                tp = conf_matrix_model_1.iloc[1, 1]
                tn = conf_matrix_model_1.iloc[0, 0]
                fp = conf_matrix_model_1.iloc[0, 1]
                fn = conf_matrix_model_1.iloc[1, 0]

                accuracy_model1 = accuracy(tp, tn, fn, fp)
                overall_error_rate_model1 = overall_error_rate(tp, tn, fn, fp)
                sensivity_model1 = sensivity(tp, fn)
                false_negative_rate_model1 = false_negative_rate(tp, fn)
                specifity_model1 = specifity(tn, fp)
                false_positive_rate_model1 = false_positive_rate(tn, fp)
                precision_model1 = precision(tp, fp)
                false_positive_propotion_model1 = false_positive_propotion(tp, fp)
                true_negative_propotion_model1 = true_negative_propotion(tn, fn)
                false_negative_propotion_model1 = false_negative_propotion(tn, fn)
                f1_score_model1 = f1_score(sensivity_model1, precision_model1)

                conf_matrix_model_2 = pd.crosstab(
                    true_values,
                    model2_preds,
                    rownames=["Rzeczywista"],
                    colnames=["Przewidywana"],
                )

                print(conf_matrix_model_2)

                tp = conf_matrix_model_2.iloc[1, 1]
                tn = conf_matrix_model_2.iloc[0, 0]
                fp = conf_matrix_model_2.iloc[0, 1]
                fn = conf_matrix_model_2.iloc[1, 0]
                accuracy_model2 = accuracy(tp, tn, fn, fp)
                overall_error_rate_model2 = overall_error_rate(tp, tn, fn, fp)
                sensivity_model2 = sensivity(tp, fn)
                false_negative_rate_model2 = false_negative_rate(tp, fn)
                specifity_model2 = specifity(tn, fp)
                false_positive_rate_model2 = false_positive_rate(tn, fp)
                precision_model2 = precision(tp, fp)
                false_positive_propotion_model2 = false_positive_propotion(tp, fp)
                true_negative_propotion_model2 = true_negative_propotion(tn, fn)
                false_negative_propotion_model2 = false_negative_propotion(tn, fn)
                f1_score_model2 = f1_score(sensivity_model1, precision_model1)

                classification_models = {}

                classification_models["Trafność"] = [
                    accuracy_model1,
                    accuracy_model2,
                    True,
                ]
                classification_models["Całkowity współczynnik błędu"] = [
                    overall_error_rate_model1,
                    overall_error_rate_model2,
                    False,
                ]
                classification_models["Czułość"] = [
                    sensivity_model1,
                    sensivity_model2,
                    True,
                ]
                classification_models["Wskaźnik fałszywie negatywnych"] = [
                    false_negative_rate_model1,
                    false_negative_rate_model2,
                    False,
                ]
                classification_models["Swoistość"] = [
                    specifity_model1,
                    specifity_model2,
                    True,
                ]
                classification_models["Wskaźnik fałszywie pozytywnych"] = [
                    false_positive_rate_model1,
                    false_positive_rate_model2,
                    False,
                ]
                classification_models["Precyzja"] = [
                    precision_model1,
                    precision_model2,
                    True,
                ]
                classification_models["Proporcja fałszywie pozytywnych"] = [
                    false_positive_propotion_model1,
                    false_positive_propotion_model2,
                    False,
                ]
                classification_models["Proporcja pozytywnie negatywnych"] = [
                    true_negative_propotion_model1,
                    true_negative_propotion_model2,
                    True,
                ]
                classification_models["Proporcja fałszywie negatywnych"] = [
                    false_negative_propotion_model1,
                    false_negative_propotion_model2,
                    False,
                ]
                classification_models["Wynik F1"] = [
                    f1_score_model1,
                    f1_score_model2,
                    True,
                ]

                data["income"] = data["income"].map({">50K": 1, "<=50K": 0})
                data["C50_PV"] = data["C50_PV"].map({">50K": 1, "<=50K": 0})
                data["rf_PV"] = data["rf_PV"].map({">50K": 1, "<=50K": 0})
                print(data)
                true_values = data["income"]

                results_window = Toplevel(self.root)
                results_window.title("Wyniki analizy klasyfikacji binarnej")
                app_results = ModelResultsApp(results_window)
                app_results.show_confusion_matrix_in_tk(
                    conf_matrix_model_1, conf_matrix_model_2
                )
                app_results.display_results_classification(
                    classification_models, model1_prob, model2_prob, true_values
                )

            except Exception:
                raise Exception("Błąd!")


class ModelResultsApp:
    def __init__(self, root):
        self.root = root

        self.models_frame = tk.Canvas(self.root)
        self.models_frame.pack(pady=10)

        self.scrollable_frame = tk.Frame(self.models_frame)

        self.model1_matrices_label = tk.LabelFrame(
            self.models_frame, text="Model 1", padx=10, pady=10
        )
        self.model1_matrices_label.pack(side="left", padx=10)

        self.model2_matrices_label = tk.LabelFrame(
            self.models_frame, text="Model 2", padx=10, pady=10
        )
        self.model2_matrices_label.pack(side="left", padx=10)

        self.conf_matrices_frame = tk.Frame(self.models_frame)
        self.conf_matrices_frame.pack(side="top")

        self.model1_conf_matrix = tk.Frame(self.conf_matrices_frame)
        self.model1_conf_matrix.pack(side="left", padx=20)

        self.model2_conf_matrix = tk.Frame(self.conf_matrices_frame)
        self.model2_conf_matrix.pack(side="left", padx=20)

        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(pady=10)

        self.model1_results = tk.LabelFrame(
            self.results_frame, text="Model 1", padx=10, pady=10
        )
        self.model1_results.pack(side="left", padx=10)

        self.model2_results = tk.LabelFrame(
            self.results_frame, text="Model 2", padx=10, pady=10
        )
        self.model2_results.pack(side="left", padx=10)

        self.chart_container = tk.Frame(self.root)
        self.chart_container.pack(pady=10)

        self.chart_frame_model1 = tk.Frame(self.chart_container)
        self.chart_frame_model1.pack(side="left", padx=10)

        self.chart_frame_model2 = tk.Frame(self.chart_container)
        self.chart_frame_model2.pack(side="left", padx=10)

        self.scrollable_frame.bind(
            "<Configure>",
            self.models_frame.configure(scrollregion=self.models_frame.bbox("all")),
        )
        self.models_frame.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        # Przewijaj canvas przy użyciu kółka myszy (Windows/macOS)
        if event.delta:
            scroll = -1 if event.delta > 0 else 1
        else:
            # Dla niektórych systemów
            scroll = event.num

        self.models_frame.yview_scroll(scroll, "units")

    def display_results_regression(
        self,
        regression_models,
        true_values,
        model1_preds,
        model2_preds,
    ):

        better_model_font = ("Helvetica", 12, "bold")
        normal_font = ("Helvetica", 12)

        for label, values in regression_models.items():
            tk.Label(
                self.model1_results,
                text=f"{label}: {values[0]:.2f}",
                font=better_model_font if values[0] < values[1] else normal_font,
            ).pack(anchor="center")

        for label, values in regression_models.items():
            tk.Label(
                self.model2_results,
                text=f"{label}: {values[1]:.2f}",
                font=better_model_font if values[0] > values[1] else normal_font,
            ).pack(anchor="center")

        draw_histogram(true_values, model1_preds, "Model1", self.chart_frame_model1)
        draw_histogram(true_values, model2_preds, "Model2", self.chart_frame_model2)

    def display_results_classification(
        self, classification_models, model1_prob, model2_prob, true_values
    ):
        better_model_font = ("Helvetica", 12, "bold")
        normal_font = ("Helvetica", 12)
        for label, values in classification_models.items():
            if values[2] and values[0] >= values[1]:
                font = better_model_font
            elif values[2] is not True and values[0] <= values[1]:
                font = better_model_font
            else:
                font = normal_font
            tk.Label(
                self.model1_results,
                text=f"{label}: {(values[0]*100):.2f}%",
                font=font,
            ).pack(anchor="w")

        for label, values in classification_models.items():
            if values[2] and values[0] <= values[1]:
                font = better_model_font
            elif values[2] is not True and values[0] >= values[1]:
                font = better_model_font
            else:
                font = normal_font
            tk.Label(
                self.model2_results,
                text=f"{label}: {(values[1]*100):.2f}%",
                font=font,
            ).pack(anchor="w")

        draw_curve_ROC(true_values, model1_prob, "Model1", self.chart_frame_model1)
        draw_curve_ROC(true_values, model2_prob, "Model2", self.chart_frame_model2)

    def show_confusion_matrix_in_tk(self, conf_matrix1, conf_matrix2):

        tk.Label(
            self.model1_matrices_label,
            text="Przewidziane ↓",
            font=("Arial", 10, "italic"),
        ).grid(row=0, column=2)
        tk.Label(
            self.model1_matrices_label,
            text="Rzeczywiste →",
            font=("Arial", 10, "italic"),
        ).grid(row=2, column=0, sticky="w")
        for j, col_name in enumerate(conf_matrix1.columns):
            tk.Label(
                self.model1_matrices_label, text=col_name, font=("Arial", 10, "bold")
            ).grid(row=1, column=j + 2, padx=5, pady=5)

        for i, row_name in enumerate(conf_matrix1.index):
            tk.Label(
                self.model1_matrices_label, text=row_name, font=("Arial", 10, "bold")
            ).grid(row=i + 2, column=1, padx=5, pady=5)
            for j, col_name in enumerate(conf_matrix1.columns):
                value = conf_matrix1.loc[row_name, col_name]
                font_style = ("Arial", 10, "bold") if i == j else ("Arial", 10)
                tk.Label(
                    self.model1_matrices_label, text=str(value), font=font_style
                ).grid(row=i + 2, column=j + 2, padx=5, pady=5)

        tk.Label(
            self.model2_matrices_label,
            text="Przewidziane ↓",
            font=("Arial", 10, "italic"),
        ).grid(row=0, column=2)
        tk.Label(
            self.model2_matrices_label,
            text="Rzeczywiste →",
            font=("Arial", 10, "italic"),
        ).grid(row=2, column=0, sticky="w")

        for j, col_name in enumerate(conf_matrix1.columns):
            tk.Label(
                self.model2_matrices_label, text=col_name, font=("Arial", 10, "bold")
            ).grid(row=1, column=j + 2, padx=5, pady=5)

        for i, row_name in enumerate(conf_matrix2.index):
            tk.Label(
                self.model2_matrices_label, text=row_name, font=("Arial", 10, "bold")
            ).grid(row=i + 2, column=1, padx=5, pady=5)
            for j, col_name in enumerate(conf_matrix2.columns):
                value = conf_matrix2.loc[row_name, col_name]
                font_style = ("Arial", 10, "bold") if i == j else ("Arial", 10)
                tk.Label(
                    self.model2_matrices_label, text=str(value), font=font_style
                ).grid(row=i + 2, column=j + 2, padx=5, pady=5)
