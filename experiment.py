import subprocess
import numpy as np
import matplotlib.pyplot as plt

# Define the noise factors to test
noise_factors = [1/64, 1/16, 1/4, 4, 16, 64]
num_trials = 10

def run_pf_data_and_filter_noise(factor, seed):
    cmd = [
        'python', 'localization.py',
        'pf',
        '--data-factor', str(factor),    # Vary data noise
        '--filter-factor', str(factor),  # Vary filter noise (same as data noise)
        '--seed', str(seed)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout

    mean_error = None
    for line in output.split('\n'):
        if 'Mean position error:' in line:
            mean_error = float(line.split(':')[-1].strip())
            break
    return mean_error

mean_errors = []

# Running trials for each noise factor
print("Running Part (b): Vary both data noise and filter noise...\n")

for r in noise_factors:
    errors = []
    print(f'Noise factor: {r}')
    for trial in range(num_trials):
        err = run_pf_data_and_filter_noise(r, trial)
        if err is not None:
            errors.append(err)
            print(f'  Trial {trial}: Mean position error = {err:.4f}')
        else:
            print(f'  Trial {trial}: Failed to parse output.')
    avg_err = np.mean(errors)
    mean_errors.append(avg_err)
    print(f'Average mean position error for factor {r}: {avg_err:.4f}\n')

# Plotting the results: Mean Position Error vs Noise Factor
fig, ax1 = plt.subplots()

# Plot mean position error (MPE)
ax1.set_xlabel('Noise Factor (α and β scaled)')
ax1.set_xscale('log')
ax1.set_ylabel('Mean Position Error', color='tab:blue')
ax1.plot(noise_factors, mean_errors, 'o-', color='tab:blue', label='Mean Position Error')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a second y-axis to plot the noise factor
ax2 = ax1.twinx()  
ax2.set_ylabel('Noise Factor (r)', color='tab:red')  
ax2.plot(noise_factors, noise_factors, 's--', color='tab:red', label='Noise Factor (r)')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Adding title and grid
plt.title('Part (b): Mean Position Error vs Noise Factor (Data and Filter Noise)')
ax1.grid(True)

# Show the plot
fig.tight_layout()
plt.show()
