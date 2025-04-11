import math
def mean_absolute_error(true,pred):
    n = len(true)
    total_error = 0
    for y_true, y_pred in zip(true,pred):
        total_error += abs(y_true - y_pred)
    return total_error / n

def mean_square_error(true,pred):
    n = len(true)
    total_error = 0
    for y_true, y_pred in zip(true,pred):
        total_error += (y_true - y_pred)**2
    return total_error / n

def root_mean_square_error(true,pred):
    return math.sqrt(mean_square_error(true,pred))

def mean_absolute_percentage_error(true,pred):
    n = len(true)
    total_error = 0
    for y_true, y_pred in zip(true,pred):
        if true != 0:
            total_error += abs((y_true - y_pred)/ y_true)
    return (100 * total_error) / n