import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from sympy import symbols, integrate, solve, log, exp

z = symbols('z', real=True, positive=True)
u = symbols('u', real=True, positive=True)

f_z = 4 * math.e ** (4 - 4 * z)
F_z = integrate(f_z, (z, 1, z))

theoretical_pdf = lambda z: 4 * math.e ** (4 - 4 * z)

exp_theor = integrate(z * f_z, (z, 1, 3))
var_theor = integrate((z**2) * f_z, (z, 1, 3)) - exp_theor**2

sample_sizes = [50, 100, 1000, 10**5]

def inverse_distribution_function(u):
    return 1 - (1/4) * np.log(1 - u)

def random_generator(size):
    u_values = np.random.uniform(0, 1, size)    
    z_values = inverse_distribution_function(u_values)    
    return z_values

samples = {n: random_generator(n) for n in sample_sizes}

sample_statistics = {n: (np.mean(samples[n]), np.var(samples[n], ddof=1)) for n in sample_sizes}

def plot_histogram(sample, n, theoretical_pdf, xlims=(1, 3)):
    plt.figure(figsize=(10, 6))
    plt.hist(sample, bins=100, density=True, alpha=0.6, label=f'Размер выборки n={n}')
    z_vals = np.linspace(xlims[0], xlims[1], 1000)
    plt.plot(z_vals, theoretical_pdf(z_vals), 'r', label='Теоретическая плотность вероятности')
    plt.xlim(xlims)
    plt.title(f'Гистограмма и теоретическая плотность вероятности для выборки объемом {n}')
    plt.xlabel('Значение')
    plt.ylabel('Плотность вероятности')
    plt.legend()
    plt.show()

def chi_square_test(sample, theoretical_pdf, bins=100, xlims=(1, 3)):
    observed_freq, bin_edges = np.histogram(sample, bins=bins, range=xlims, density=True)
    observed_freq = observed_freq.astype('float')
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    expected_freq = theoretical_pdf(bin_centers) * (bin_edges[1] - bin_edges[0]) * len(sample)
    chi2_stat, p_value = chi2_contingency([observed_freq, expected_freq])[0:2]
    return chi2_stat, p_value

chi_square_results = {n: chi_square_test(samples[n], theoretical_pdf, bins=20) for n in sample_sizes}

print("Математическое ожидание и дисперсия для каждой выборки:")
print(sample_statistics)

print("\nАналитически рассчитанные математическое ожидание и дисперсия:")
print(exp_theor, var_theor)

print("\nРезультаты критерия Пирсона:")
print(chi_square_results)

for n in sample_sizes:
    plot_histogram(samples[n], n, theoretical_pdf)