import timeit as tm

print(tm.timeit(stmt="np.random.choice([-1, 1], (64, 64, 64))", setup="import numpy as np", number=1_000))
print(tm.timeit(stmt="np.random.choice([-1, 1], (64**3))", setup="import numpy as np", number=1000))
