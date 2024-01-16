import numpy as np
import matplotlib.pyplot as plt

def system(t, x):
    x1, x2, x3, x4, x5 = x
    b = np.where(np.abs(x[1]) <= 0.5, x[1], 0.5)
    dx1dt = 2 * x2 - 2 * x1
    dx2dt = x3
    dx3dt = 7 * x1 - 7 * x2 - 1 * x3 + 9 * x4
    dx4dt = b
    dx5dt = 700 * np.sin(x1)
    return np.array([dx1dt, dx2dt, dx3dt, dx4dt, dx5dt])

def relative_error(teta, x2, x5):
    return -110 * x2 - 18 * x2 - 2 * x5 + 150 * (teta - x2)

def runge_kutta(h, T):
    num_steps = int(T / h)
    t_values = np.linspace(0, T, num_steps + 1)
    x_values = np.zeros((num_steps + 1, 5))
    delta_values = np.zeros(num_steps + 1)

    # Initial conditions
    x_values[0] = [0.3, 0.3, 0, 0, 500]
    delta_values[0] = x_values[0, 3]

    for i in range(1, num_steps + 1):
        k1 = h * system(t_values[i - 1], x_values[i - 1])
        x1_temp = x_values[i - 1] + k1
        k2 = h * system(t_values[i - 1] + h, x1_temp)
        x_values[i] = x_values[i - 1] + 0.5 * (k1 + k2)
        delta_values[i] = relative_error((10000 - x_values[i, 4]) / (27000 - 700 * t_values[i]), x_values[i, 1], x_values[i, 4])

    return t_values, x_values, delta_values

def plot_results(t_values, x_values, delta_values):
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t_values, x_values[:, 4], label='x5(t)')
    plt.title('Variable State x5(t)')
    plt.xlabel('Time (s)')
    plt.ylabel('x5(t)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(t_values, delta_values, label='Relative Error (δ)')
    plt.title('Relative Error δ')
    plt.xlabel('Time (s)')
    plt.ylabel('δ')
    plt.legend()

    plt.tight_layout()
    plt.show()

def analyze_accuracy_efficiency(h_values, T):
    errors = []
    computational_costs = []

    for h in h_values:
        t_values, x_values, delta_values = runge_kutta(h, T)
        errors.append(np.max(np.abs(delta_values)))
        computational_costs.append(len(t_values))

    plt.figure(figsize=(10, 6))
    plt.plot(h_values, errors, label='Max Relative Error (δ)')
    plt.title('Accuracy vs. Step Size')
    plt.xlabel('Step Size (h)')
    plt.ylabel('Max Relative Error (δ)')
    plt.xscale('log')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(h_values, computational_costs, label='Computational Cost')
    plt.title('Computational Cost vs. Step Size')
    plt.xlabel('Step Size (h)')
    plt.ylabel('Computational Cost (Number of Steps)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.show()

def automatic_step_selection(T):
    h_values = [0.01, 0.005, 0.001, 0.0005, 0.0001]
    errors = []

    for h in h_values:
        t_values, x_values, delta_values = runge_kutta(h, T)
        errors.append(np.max(np.abs(delta_values)))

    best_h = h_values[np.argmin(errors)]
    t_values, x_values, delta_values = runge_kutta(best_h, T)

    plt.figure(figsize=(12, 8))
    plt.plot(t_values, x_values[:, 4], label='x5(t)')
    plt.title(f'Variable State x5(t) with Automatic Step Selection (h={best_h})')
    plt.xlabel('Time (s)')
    plt.ylabel('x5(t)')
    plt.legend()
    plt.show()

    print(f"Automatic Step Selection Results (h={best_h}):")
    print(f"Max Relative Error (δ): {np.max(np.abs(delta_values))}")
    print(f"Number of Steps: {len(t_values)}")

# Main part of the script
T = 10  # Total integration time

# Task 1: Solve the system and plot the results
t_values, x_values, delta_values = runge_kutta(0.01, T)
plot_results(t_values, x_values, delta_values)

# Task 2: Analyze accuracy and efficiency
h_values_to_analyze = [0.1, 0.05, 0.01, 0.005, 0.001]
analyze_accuracy_efficiency(h_values_to_analyze, T)

# Task 3: Automatic step selection
automatic_step_selection(T)
