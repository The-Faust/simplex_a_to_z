from numpy import array
from scipy.optimize import linprog
from simplex_modular_implementation.utilities import print_infos_on_simplex_run
from simplex_modular_implementation.revised_simplex import \
    create_solvable_matrix, create_phase_1_matrix, find_possible_column_index, \
    find_possible_line_index, find_line_and_column_index_for_pivot, phase_1_special_pivot, two_phase_simplex

#solvable_matrix_part_a = array([
#    [-1, 1, -4, 4, 1],
#    [-1, 1, 1, -1, -2],
#    [1, 3, 2, -2, 3],
#    [-1, -3, -2, 2, -3],
#    [2, -1, 1, -1, 0]
#])

A = array([
    [-1, 1, -4, 4],
    [-1, 1, 1, -1],
    [1, 3, 2, -2],
    [-1, -3, -2, 2]
])

b = array([1, -2, 3, -3])
c = array([2, -1, 1, -1])

print(linprog(c, A_ub=A, b_ub=b))

solvable_matrix = create_solvable_matrix(A=A, b=b, c=c)

summit_list = two_phase_simplex(solvable_matrix, opt_max=False)

print_infos_on_simplex_run(summit_list)
