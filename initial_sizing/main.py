import numpy as np
import pandas as pd

from pymoo.algorithms.nsga2 import NSGA2
from pymoo.model.problem import Problem
from pymoo.optimize import minimize
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
from pymoo.util.termination.default import MultiObjectiveDefaultTermination
from pymoo.visualization.scatter import Scatter

import matplotlib.pyplot as plt

# import analysis_02
import analysis_01

class MyProblem(Problem):

    def __init__(self):
        super().__init__(n_var=4,
                         n_obj=2,
                         n_constr=6,
                         xl=np.array([100, 3, 5, 2.0]),
                         xu=np.array([350, 170, 12, 4.0]),
                        # xl=np.array([100, 100, 5, 26, 30, 2]),
                        # xu=np.array([350, 250, 12, 32, 45, 10]),
                        elementwise_evaluation=True)

    def _evaluate(self, x, out, *args, **kwargs):
        (f1, f2, g_3_aux, g_4_aux, g_5_aux, g_6_wing_load_given, g_6_max_wing_load, rotor_diameter) = analysis_01.main(x[0], x[1], x[2], x[3])

        # (f1, f2, g_3_aux, g_4_aux, g_5_aux, g_6_wing_load_given, g_6_max_wing_load, g_7_stall_speed_given,
        # g_7_cruise_speed_given, rotor_diameter) = analysis_02.main(x[0], x[1], x[2], x[3], x[4], x[5])

        g1 = f1 - 25
        g2 = -(f2 - 2.5)
        g3 = g_3_aux - 0.175 # Fuel Mass cannot exceed tank mass capacity
        g4 = g_4_aux - 1300  # Fuel Cell nominal power
        g5 = g_5_aux - 4     # Max. wingspan of 4 [m]
        g6 = g_6_wing_load_given - g_6_max_wing_load
        # g7 = g_7_stall_speed_given - g_7_cruise_speed_given + 8 
        # g7 = g_6_stall_speed_given - g_8_loiter_speed_given + 8

        out["F"] = [f1, -f2]
        out["G"] = [g1, g2, g3, g4, g5, g6]
        # out["G"] = [g1, g2, g3, g4, g5, g6, g7]


vectorized_problem = MyProblem()

algorithm = NSGA2(
    pop_size=200,
    eliminate_duplicates=True
)

stopping_criteria = MultiObjectiveDefaultTermination(
    x_tol=5e-4,
    cv_tol = 1e-6,
    f_tol = 1e-3,
    n_max_gen = 150
)

res = minimize(vectorized_problem,
               algorithm,
               stopping_criteria,
               verbose=True,
               seed=1,
               save_history=True)

_F = res.F
ideal = _F.min(axis=0)
nadir = _F.max(axis=0)

for gen, algorithm in enumerate(res.history, start=1):

    # if gen == 1:
    #     pass
    
    # elif gen == 5:
    #     pass

    # elif gen == 17:
    #     pass

    # elif gen == 70:
    #     pass

    # elif gen == 90:
    #     pass

    # elif gen == 115:
    #     pass

    # else:
    #     continue

    F = algorithm.pop.get("F")

    nds = NonDominatedSorting().do(F, only_non_dominated_front=True)
    other = [i for i in range(len(F)) if i not in nds]

    plt.scatter(F[nds, 0], F[nds, 1], facecolor="none", edgecolor="blue", s=100, linewidths=2, marker = 'o', label='Non-Dominated Solutions')
    plt.scatter(F[other, 0], F[other, 1], facecolor="none", edgecolor="red", s=100, linewidths=2, marker = 'v', label='Dominated Solutions')
    plt.title(f"Generation {algorithm.n_gen}", fontsize=16)

    plt.xlim(ideal[0], nadir[0])
    plt.xticks(fontsize=14)
    plt.xlabel('MTOM in kg', fontsize=14)  # Add an x-label to the axes.

    plt.ylim(ideal[1], nadir[1])
    plt.yticks(fontsize=14)
    plt.ylabel('-Endurance in h', fontsize=14)  # Add a y-label to the axes.

    if gen == 1:
        plt.legend(fontsize = 14)  # Add a legend.

    plt.draw()
    plt.waitforbuttonpress()
    # plt.savefig(f'Convergence_Study_Gen{gen}.pdf')
    # plt.pause(0.25)
    plt.clf()

plt.close()

plot = Scatter()
plot.add(vectorized_problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, color="red")
plot.show()

arr = np.concatenate((res.F, res.X, res.G[:, 2:4]), axis=1)

data = pd.DataFrame(arr, 
                    columns=[
                        'MTOW [Kg]', '-Endurance [h]', 'Disk Loading [N/m2]', 'Wing Loading [N/m2]', 
                        'Wing Aspect Ratio', 'Loiter Time [h]', '3rd Constraint Violation Value',
                        '4th Constraint Violation Value'
                    ])


# data = pd.DataFrame(arr, 
#                     columns=[
#                         'MTOW [Kg]', '-Endurance [h]', 'Disk Loading [N/m2]', 'Wing Loading [N/m2]', 
#                         'Wing Aspect Ratio', 'Stall Speed [m/s]', 'Operational Speed [m/s]', 
#                         'Loiter Time [h]', '3rd Constraint Violation Value', '4th Constraint Violation Value'
#                     ])

ordered_data = data.sort_values(by ='MTOW [Kg]', axis=0, ascending = True)

ordered_data['Wing Area [m2]'] = ordered_data['MTOW [Kg]'] * 9.81 / ordered_data['Wing Loading [N/m2]']
ordered_data['Wingspan [m]'] = np.sqrt(ordered_data['Wing Area [m2]'] * ordered_data['Wing Aspect Ratio'])
ordered_data['Max. Lvl Flight Power [W]'] = ordered_data['4th Constraint Violation Value'] + 1300
ordered_data['Rotor Area [m2]'] = ordered_data['MTOW [Kg]'] * 9.81 / ordered_data['Disk Loading [N/m2]']

# save the pandas dataframe as a csv file
ordered_data.to_csv("pareto_data_big.csv", sep=';')

print(type(res.F))
print(res.F)
print(res.X)
print(res.G)
print(ideal)

# print(main(5.5, 10, 0.08, 2))