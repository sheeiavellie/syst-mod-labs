import numpy as np
import math
import random
import matplotlib.pyplot as plt

# Данные
D = 2
alpha = 1.5
h = 0.005
t_max = 3 / alpha
S0 = h / 12
Kf = np.sqrt((2 * D) / alpha / S0)
Tf = 1 / alpha
size = 10000
steps = math.floor((0 + t_max) / h)

# Функции
def white_noise(size):
    white_noise = [random.random() - 0.5 for _ in range(size)]
    return white_noise

def exp_val_and_random_process(Kf, Tf, white_noise, h, size):
    random_process = np.zeros(size)
    temp = 0

    for i in range(size - 1):
        random_process[i + 1] = random_process[i] + h * ((Kf / Tf) * white_noise[i] - (1 / Tf) * random_process[i])
        temp += random_process[i + 1]
    
    exp_val = temp / size

    return exp_val, random_process

def true_correlation_function(D, alpha, h, steps):
    theoretical_correlation = [
        D * np.exp(-alpha * i * h) for i in range(steps)
        ]
    return theoretical_correlation

def computed_correlation_function(alpha, h, size, rand_process, exp_val, steps):
    computed_correlation = []

    for j in range(int(steps)):
        total = 0
        for i in range(size - j):
            total += (rand_process[i] - exp_val) * (rand_process[i + j] - exp_val)
        total /= size + 1 - j
        computed_correlation.append(total)
    return computed_correlation

# Вычисления
t_values = np.arange(0, t_max, h)

white_noise = white_noise(size)
exp_val, random_process = exp_val_and_random_process(Kf, Tf, white_noise, h, size)

true_correlation_values = true_correlation_function(D, alpha, h, steps)
computed_correlation_values = computed_correlation_function(alpha, h, size, random_process, exp_val, steps)

tau_values = np.arange(0, t_max, h)

# Графики
plt.figure(figsize=(12, 6))

# # График теоретической корреляционной функции
# plt.subplot(3, 1, 1)
# plt.plot(t_values, true_correlation_values, label='График заданной корреляционной функции')
# plt.title('График заданной корреляционной функции')
# plt.xlabel('𝜏')
# plt.ylabel('K(𝜏)')

# # График полученной корреляционной функции
# plt.subplot(3, 1, 2)
# plt.plot(tau_values, computed_correlation_values, label='Computed Correlation Function')
# plt.title('График полученной корреляционной функции')
# plt.xlabel('𝜏')
# plt.ylabel('K(𝜏)')

# График теоретической и полученной корреляционных функций
#plt.subplot(3, 1, 3)
plt.plot(t_values, true_correlation_values, label='Теоретическая корреляционная функция', color='magenta')
plt.plot(tau_values, computed_correlation_values, label='Полученная корреляционная функция', color='cyan')
plt.title('График теоретической и полученной корреляционных функций')
plt.xlabel('𝜏')
plt.ylabel('K(𝜏)')
plt.legend()

plt.tight_layout()
plt.show()
