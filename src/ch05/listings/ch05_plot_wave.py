import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, N, 50)
wave = [1/sqrt(8)*cos(2 * pi * frequency * (t/N)) for t in x]
plt.plot(x, wave, label='signal', color='red')
plt.scatter(range(N), samples)
plt.show()