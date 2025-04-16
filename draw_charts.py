import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def draw_histogram(true_values, preds_values, model_name, parent_frame):
    errors = [true - pred for true, pred in zip(true_values, preds_values)]
    mean = sum(errors) / len(errors)
    std_dev = math.sqrt(sum((e - mean) ** 2 for e in errors) / len(errors))

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    # Histogram
    ax.hist(
        errors,
        bins=30,
        density=True,
        alpha=0.6,
        color="skyblue",
        label="Histogram błędów",
    )

    # Normal Curve
    x_vals = np.linspace(min(errors), max(errors), 100)
    normal_curve = [
        (1 / (std_dev * math.sqrt(2 * math.pi)))
        * math.exp(-((x - mean) ** 2) / (2 * std_dev**2))
        for x in x_vals
    ]
    ax.plot(x_vals, normal_curve, color="red", label="Krzywa normalna")

    ax.set_title(f"Błędy - {model_name}")
    ax.set_xlabel("Błąd")
    ax.set_ylabel("Gęstość")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def draw_curve_ROC(y_true, y_prob, model_name, parent_frame):

    data = list(zip(y_prob, y_true))
    data.sort(reverse=True)

    T = sum(y_true)
    N = len(y_true) - T

    tpr_list = []
    fpr_list = []

    tp = fp = 0

    for prob, label in data:
        if label == 1:
            tp += 1
        else:
            fp += 1
        tpr = tp / T
        fpr = fp / N
        tpr_list.append(tpr)
        fpr_list.append(fpr)

    auc_value = 0
    for i in range(1, len(tpr_list)):
        auc_value += (
            (fpr_list[i] - fpr_list[i - 1]) * (tpr_list[i] + tpr_list[i - 1]) / 2
        )
    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)

    ax.plot(fpr_list, tpr_list, label=f"ROC (AUC = {auc_value:.2f})")
    ax.plot([0, 1], [0, 1], "k--")
    ax.set_xlabel("Wskaźnik fałszywie pozytywnych (1 - Specyficzność)")
    ax.set_ylabel("Wskaźnik prawdziwie pozytywnych (Czułość)")
    ax.set_title(f"Krzywa ROC - {model_name}")
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
