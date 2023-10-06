from math import atan2

a = abs(f)
d = [atan2(c.imag, c.real) for c in f]
fig, axs = plt.subplots(int(N/2)+1)
for k in range(int(N/2)+1):
    axs[k].plot(x, [(1/N if k == 0 or k == N/2 else 2/N) * a[k] * cos(2 * pi / N * k*j + d[k]) for j in x])
plt.show()