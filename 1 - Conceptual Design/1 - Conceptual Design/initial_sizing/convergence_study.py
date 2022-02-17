from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
from pymoo.visualization.scatter import Scatter

import matplotlib.pyplot as plt

problem = get_problem("zdt1")

algorithm = NSGA2(pop_size=100)

res = minimize(problem,
               algorithm,
               ('n_gen', 200),
               seed=1,
               verbose=True,
               save_history=True)

_F = res.F
ideal = _F.min(axis=0)
nadir = _F.max(axis=0)

for algorithm in res.history:
    F = algorithm.pop.get("F")

    nds = NonDominatedSorting().do(F, only_non_dominated_front=True)
    other = [i for i in range(len(F)) if i not in nds]

    plt.scatter(F[nds, 0], F[nds, 1], facecolor="none", edgecolor="blue")
    plt.scatter(F[other, 0], F[other, 1], facecolor="none", edgecolor="red")
    plt.title(f"Generation {algorithm.n_gen}")

    plt.xlim(ideal[0], nadir[0])
    plt.ylim(ideal[1], nadir[1])

    plt.draw()
    plt.waitforbuttonpress()
    # plt.pause(0.25)
    plt.clf()

plt.close()

plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, color="red")
plot.show()