import math

def uncertainty(raw_data_string):
    clean_string = raw_data_string.replace('\t', ' ').replace(',', '.')

    tokens = clean_string.split()

    values = [float(x) for x in tokens]
    n = len(values)

    if n < 2:
        raise ValueError("Insufficient data: Insert at least 2 values.")
    
    mean = sum(values)/n
    variance = sum((x-mean) ** 2 for x in values) / (n-1)
    std_dev = math.sqrt(variance)
    uncertainty_mean = std_dev / math.sqrt(n)

    return n, mean, std_dev, uncertainty_mean