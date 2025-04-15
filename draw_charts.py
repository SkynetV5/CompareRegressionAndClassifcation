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
    ax.hist(errors, bins=30, density=True, alpha=0.6, color="skyblue", label="Histogram błędów")

    # Krzywa normalna
    x_vals = np.linspace(min(errors), max(errors), 100)
    normal_curve = [(1 / (std_dev * math.sqrt(2 * math.pi))) * math.exp(-((x - mean) ** 2) / (2 * std_dev ** 2)) for x
                    in x_vals]
    ax.plot(x_vals, normal_curve, color='red', label='Krzywa normalna')

    ax.set_title(f"Błędy - {model_name}")
    ax.set_xlabel("Błąd")
    ax.set_ylabel("Gęstość")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

