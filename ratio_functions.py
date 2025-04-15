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
        total_error += abs((y_true - y_pred)/ y_true)
    return (100 * total_error) / n

def accuracy(tp,tn,fn,fp):
    return (tp + tn) / (tp + tn + fn + fp)

def overall_error_rate(tp,tn,fn,fp):
    return (fp + fn) / (tp + tn + fn + fp)

def sensivity(tp,fn):
    return tp / (fn + tp)

def false_negative_rate(tp,fn):
    return fn / (fn + tp)

def specifity(tn,fp):
    return tn / (fp + tn)

def false_positive_rate(tn,fp):
    return fp / (fp + tn)

def precision(tp,fp):
    return tp / (fp + tp)

def false_positive_propotion(tp,fp):
    return fp / (fp + tp)

def true_negative_propotion(tn,fn):
    return tn / (fn + tn)

def false_negative_propotion(tn,fn):
    return fn / (fn + tn)

def f1_score(sensivity,precision):
    return 2 * ((sensivity * precision)/(sensivity + precision))


