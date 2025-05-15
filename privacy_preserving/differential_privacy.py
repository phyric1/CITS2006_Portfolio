import pandas as pd
import numpy as np
import argparse

def laplace_mechanism(value, sensitivity, epsilon):
    noise = np.random.laplace(0, sensitivity / epsilon)
    return round(value + noise)

# Command-line arguments
parser = argparse.ArgumentParser(description="Apply Local Differential Privacy to medical data.")
parser.add_argument("input_csv", help="Path to input CSV file")
parser.add_argument("output_csv", help="Path to output CSV file")
parser.add_argument("--epsilon", type=float, default=1.0, help="Privacy budget (default: 1.0)")

args = parser.parse_args()

# Parameters
epsilon = args.epsilon
hr_sensitivity = 10
bp_systolic_sensitivity = 15
bp_diastolic_sensitivity = 10

df = pd.read_csv(args.input_csv)

df['heart_rate'] = df['heart_rate'].apply(lambda x: laplace_mechanism(x, hr_sensitivity, epsilon))
df['blood_pressure_systolic'] = df['blood_pressure_systolic'].apply(lambda x: laplace_mechanism(x, bp_systolic_sensitivity, epsilon))
df['blood_pressure_diastolic'] = df['blood_pressure_diastolic'].apply(lambda x: laplace_mechanism(x, bp_diastolic_sensitivity, epsilon))

df.to_csv(args.output_csv, index=False)
print(f"Noisy medical data saved to: {args.output_csv} (epsilon = {epsilon})")