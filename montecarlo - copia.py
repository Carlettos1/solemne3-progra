from math import exp

import matplotlib.pyplot as plt
import numpy as np

length = 32
J = 1
steps = 1_000


#  interacción entre los vecinos
def hamiltoniano(S, J=J):
    suma = 0
    a = length - 1
    for x in range(a):
        for y in range(a):
            for z in range(a):
                # cubo interno
                suma += S[x, y, z]*(S[x+1, y, z] + S[x, y+1, z] + S[x, y, z+1])
                pass
            # paredes laterales
            suma += S[a, x, y]*(S[a, x+1, y] + S[a, x, y+1])
            suma += S[y, a, x]*(S[y, a, x+1] + S[y+1, a, x])
            suma += S[x, y, a]*(S[x+1, y, a] + S[x, y+1, a])
            pass
        # aristas externas
        suma += S[a, a, x]*S[a, a, x+1] + S[a, x, a]*S[a, x+1, a] + S[x, a, a]*S[x+1, a, a]
        pass
    return -J*suma
    pass


estado_inicial = []
estado_final = []
ENERGIAS = []
MAGNETIZACIONES = []
for t in np.linspace(0.1, 4.0, 40):
    S = np.random.choice([-1, 1], (length, length, length))
    Energías = [hamiltoniano(S)]
    beta = 1/t
    estado_inicial.append(S.copy())

    for s in range(steps):
        k = np.random.randint(0, length)
        S[k] *= -1
        hamiltoniano_antes = Energías[-1]
        hamiltoniano_despues = hamiltoniano(S)

        if hamiltoniano_despues < hamiltoniano_antes:
            Energías.append(hamiltoniano_despues)
            pass
        elif np.random.rand() < exp(-beta*(hamiltoniano_despues - hamiltoniano_antes)):
            Energías.append(hamiltoniano_despues)
            pass
        else:
            S[k] *= -1
            Energías.append(hamiltoniano_antes)
            pass
        if s % 100 == 0:
            print(f"step: {s}")
        pass
    emean = sum(Energías)/len(Energías)/length**3
    magnetizacion = abs(np.sum(S)/length**3)
    ENERGIAS.append(emean)
    MAGNETIZACIONES.append(magnetizacion)
    estado_final.append(S)
    print(f"Energía promedio del sistema: {emean}, Temperatura: {t}, Magnetización {magnetizacion}")

fig = plt.figure()
ax = fig.add_subplot(221, projection="3d")
x, y, z = (estado_inicial[0] == 1).nonzero()
ax.scatter(x, y, z, c="#0000ffa0")
x, y, z = (estado_inicial[0] == -1).nonzero()
ax.scatter(x, y, z, c="#ff0000a0")

ax = fig.add_subplot(222, projection="3d")
x, y, z = (estado_final[0] == 1).nonzero()
ax.scatter(x, y, z, c="#0000ffa0")
x, y, z = (estado_final[0] == -1).nonzero()
ax.scatter(x, y, z, c="#ff0000a0")

ax = fig.add_subplot(222)
ax.scatter(np.linspace(0.1, 4.0, 40), MAGNETIZACIONES, label="magnetizaciones")
ax.scatter(np.linspace(0.1, 4.0, 40), ENERGIAS, label="energías")
ax.legend()
plt.show()
pass
