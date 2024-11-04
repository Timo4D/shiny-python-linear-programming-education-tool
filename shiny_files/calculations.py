
from scipy.optimize import milp, LinearConstraint
import numpy as np


def solve_linear_programming_problem(target_function, side_functions):

    upper_borders_list = []
    lower_borders_list = []

    target_coeff_1 = target_function[1]
    target_coeff_2 = target_function[3]
    if target_function[5] == "max":
        target_coeff_1 = target_coeff_1 * (-1)
        target_coeff_2 = target_coeff_2 * (-1)


    side_functions_coeff_list = []
    for function in side_functions:
        side_functions_coeff_list.append([function[1], function[3]])




        upper_borders_list.append(function[6])
        if function[5] == "≤":
            lower_borders_list.append(-np.inf)
        elif function[5] == "=" or function[5] == "≥":
            lower_borders_list.append(function[6])
            upper_borders_list[(len(upper_borders_list)-1)] = np.inf





    target_function_coefficients = np.array([target_coeff_1, target_coeff_2])
    side_function_coefficients = np.array(side_functions_coeff_list)
    all_functions_upper_border = np.array(upper_borders_list)
    all_functions_lower_border = np.array(lower_borders_list)
    problem_constraints = LinearConstraint(side_function_coefficients, all_functions_lower_border, all_functions_upper_border)

    problem_result = milp(target_function_coefficients, constraints= problem_constraints)

    print(problem_result.message)
    print(-problem_result.fun)
    print(problem_result.x)

    return [-problem_result.fun, problem_result.x]

