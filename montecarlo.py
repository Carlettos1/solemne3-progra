from math import exp

import matplotlib.pyplot as plt
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
t = (rank + 1)/10.0
# np.random.seed(69)
length = 32
J = 1
steps = 1_000
np.random.seed(69)


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


S = np.random.choice([-1, 1], (length, length, length))
Energías = [hamiltoniano(S)]
beta = 1/t

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
        print(f"rank: {rank}, step: {s}")
    pass
emean = sum(Energías)/len(Energías)/length**3
magnetizacion = abs(np.sum(S)/length**3)
print(f"Energía promedio del sistema: {emean}, Temperatura: {t}, Magnetización {magnetizacion}")

data = comm.gather((t, emean, magnetizacion))
if rank == 0:
    temps = []
    means = []
    magns = []
    for (e1, e2, e3) in data:
        temps.append(e1)
        means.append(e2)
        magns.append(e3)
    plt.scatter(temps, means, label="Energías")
    plt.scatter(temps, magns, label="Magnetismo")
    plt.legend()
    plt.show()
    pass
