import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y1= np.sin(x)
y2 = np.cos(x)

plt.figure(figsize=(8,4))
plt.plot(x, y1, 'b--', label='sin(x)')
plt.plot(x, y2, 'r--', label='cos()')
plt.title('Funções Seno e Cosseno')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.savefig('grafico.png')
plt.show()