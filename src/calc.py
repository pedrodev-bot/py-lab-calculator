import math

# --- 1. STATISTICS MODULE ---
# Calculate simple uncertainty (Type A) of a single dataset.
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

# --- 2. ERROR PROPAGATION MODULE ---
def propagate_subtraction(sigma_x, sigma_y):
    return math.sqrt(sigma_x**2 + sigma_y**2)

def propagate_inverse(x, sigma_x):
    return sigma_x/(x**2)

def propagate_multiplication(z, x, sigma_x, y, sigma_y):
    return z*math.sqrt((sigma_x/x)**2 + (sigma_y/y)**2)

# --- 3. PHYSICS SPECIFIC MODULE ---
# Calculates C_capacitor = C_measurement - C_residual.
def calculate_capacitance_corrected(c_measurement, c_residual, sigma_measurement, sigma_residual):
    c_capacitor = c_measurement - c_residual
    sigma_c = propagate_subtraction(sigma_measurement, sigma_residual)
    return c_capacitor, sigma_c

# Calculates epsilon_0 = a / Area, where Area = pi * (D/2)^2.
def calculate_permittivity(a, sigma_a, diameter, sigma_d):
    area = math.pi * (diameter/2)**2
    epsilon = a/area

    # Propagated error for epsilon = a / Area.
    # Rel_error = sqrt((sigma_a/a)^2 + (2*sigma_d/d)^2).
    rel_error = propagate_multiplication(1, a, sigma_a, diameter, sigma_d)
    sigma_epsilon = epsilon * rel_error

    return epsilon, sigma_epsilon

# Calculates linear regression (y = ax + b) weighted by uncertainty.
def linear_least_squares(x_list, y_list, sigma_y_list):
    weights = [1 / (s**2) for s in sigma_y_list]
    sum_w = sum(weights)
    
    x_mean = sum(x * w for x, w in zip(x_list, weights)) / sum_w
    y_mean = sum(y * w for y, w in zip(y_list, weights)) / sum_w
    x2_mean = sum((x**2) * w for x, w in zip(x_list, weights)) / sum_w
    xy_mean = sum(x * y * w for x, y, w in zip(x_list, y_list, weights)) / sum_w
    
    denominator = x2_mean - (x_mean**2)
    a = (xy_mean - (x_mean * y_mean)) / denominator
    b = y_mean - a * x_mean
    
    sigma_a = math.sqrt( (1/sum_w) / denominator )
    sigma_b = math.sqrt( (x2_mean/sum_w) / denominator )
    
    return a, sigma_a, b, sigma_b

# --- 4. DOCUMENTATION MODULE (Productivity) ---
# Returns LaTeX strings for report documentation.
# Usage: Paste these into your report to demonstrate calculations.
def get_formula_string(operation):
    formulas = {
        "subtraction": r"\sigma_{C} = \sqrt{\sigma_{medida}^2 + \sigma_{residual}^2}",
        "inverse": r"\sigma_{w} = \frac{\sigma_{d}}{\bar{d}^2}",
        "mean_d": r"\bar{d} = \frac{d_1 + d_2 + d_3}{3}"
    }
    return formulas.get(operation, "Formula not found")

# --- 5. DATA PROCESSING MODULE ---
# Processes al rows for Table 1 (Report 2).
# Returns a list of tuples: (d_mean, sigma_d, c_capacitor, sigma_c).
def process_table1(d1_list, d2_list, d3_list, c_medida_list, sigma_medida_list, c_residual, sigma_residual):
    results = []
    for i in range(len(d1_list)):
        # Calculate mean distance.
        d_vals = [d1_list[i], d2_list[i], d3_list[i]]
        d_mean = sum(d_vals) / 3
        # Estimate sigma_d as half the range of measurements.
        sigma_d = (max(d_vals) - min(d_vals)) / 2 if len(d_vals) > 1 else 0.01 
        
        # Calculate capacitance.
        c_cap, sigma_c = calculate_capacitance_corrected(c_medida_list[i], c_residual, sigma_medida_list[i], sigma_residual)
        results.append((d_mean, sigma_d, c_cap, sigma_c))
    return results

# Processes all rows for Table 2 (w = 1/d).
# Returns a list of tuples: (w, sigma_w, c_capacitor, sigma_c).
def process_table2(d_mean_list, sigma_d_list, c_cap_list, sigma_c_list):
    results = []
    for i in range(len(d_mean_list)):
        d = d_mean_list[i]
        sd = sigma_d_list[i]
        
        w = 1 / d
        sigma_w = propagate_inverse(d, sd)
        
        results.append((w, sigma_w, c_cap_list[i], sigma_c_list[i]))
    return results