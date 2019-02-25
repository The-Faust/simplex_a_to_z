"""
these are all the steps put into functions for the simplex method
"""
import numpy as np


def select_pivot_column(solvable_matrix, opt_max=True):
    select_column_vector = solvable_matrix[-1, :-1]
    if opt_max:
        selected_value = np.amax(select_column_vector)
    else:
        selected_value = np.amin(select_column_vector)
    return np.where(select_column_vector == selected_value)[0][0]


def select_pivot_line(solvable_matrix, column_index=0):
    line_select_numerator_array = solvable_matrix[:-1, -1]
    line_select_denominator_array = solvable_matrix[:-1, column_index]
    line_select_denominator_array[line_select_denominator_array == 0] = 0.00000000001
    line_select_quotient_criteria_array = np.divide(
        line_select_numerator_array, line_select_denominator_array)
    return np.where(line_select_quotient_criteria_array == np.amin(
        line_select_quotient_criteria_array[line_select_quotient_criteria_array > 0.000000000001]))[0][0]


def lets_pivot(solvable_matrix, line_index=0, column_index=0):
    solvable_matrix[line_index] = solvable_matrix[line_index]/solvable_matrix[line_index, column_index]
    for i in range(len(solvable_matrix)):
        if i != line_index:
            coefficient_line = (solvable_matrix[i][column_index]/solvable_matrix[line_index][column_index])
            solvable_matrix[i] = np.subtract(solvable_matrix[i], (coefficient_line * solvable_matrix[line_index]))


def find_base_indexes(solvable_matrix):
    indexes = dict()
    for column_index in range(len(solvable_matrix[-1]) - 1):
        if np.count_nonzero(solvable_matrix[:, column_index] == 1.0) ==1 and \
                (np.count_nonzero(solvable_matrix[:, column_index] == 0.0)) == len(solvable_matrix[:, column_index]) -1:
            indexes[np.where(solvable_matrix[:, column_index] == 1)[0][0]] = column_index
    return indexes


def update_base_indexes(base_indexes, new_pivot_line_index=0, new_pivot_column_index=0):
    base_indexes[new_pivot_line_index] = new_pivot_column_index


def from_base_indexes_find_solution_vector(solvable_matrix, current_base_indexes):
    assert isinstance(current_base_indexes, dict)
    summit = np.zeros(len(solvable_matrix.T) - 1)
    for line_index in current_base_indexes.keys():
        summit[current_base_indexes[line_index]] = solvable_matrix[line_index, -1]
    return summit


def is_max(solvable_matrix):
    if np.amax(solvable_matrix[-1]) <= 0.0000000000000000000001:
        return True
    return False


def is_min(solvable_matrix):
    if np.amin(solvable_matrix[-1]) >= -0.000000000000000000001:
        return True
    return False


def _packaged_simplex_steps(solvable_matrix, base_indexes, opt_max=True, prints=False):
    pivot_column_index = select_pivot_column(solvable_matrix, opt_max)
    pivot_line_index = select_pivot_line(solvable_matrix, pivot_column_index)
    update_base_indexes(base_indexes, pivot_line_index, pivot_column_index)
    lets_pivot(solvable_matrix, pivot_line_index, pivot_column_index)
    if prints:
        print("current pivot is : \n [", pivot_line_index, ", ", pivot_column_index, '] \n\n',
              "current state of solving matrix : \n", solvable_matrix, "\n\n",
              )


def simplex_that_system(solvable_matrix, opt_max=True, max_iteration=100, prints=False, is_phase_1=False):
    summits_list = list()
    base_indexes = find_base_indexes(solvable_matrix)
    if not is_phase_1:
        summits_list.append(from_base_indexes_find_solution_vector(solvable_matrix, base_indexes))

    if opt_max:
        for i in range(max_iteration):
            if not is_max(solvable_matrix):
                _packaged_simplex_steps(solvable_matrix, base_indexes, opt_max, prints=prints)
                if not is_phase_1:
                    summits_list.append(from_base_indexes_find_solution_vector(solvable_matrix, base_indexes))
            else:
                print("reached_max \n")
                break

    elif not opt_max:
        for i in range(max_iteration):
            if not is_min(solvable_matrix):
                _packaged_simplex_steps(solvable_matrix, base_indexes, opt_max, prints=prints)
                if not is_phase_1:
                    summits_list.append(from_base_indexes_find_solution_vector(solvable_matrix, base_indexes))
            else:
                print("reached_min \n")
                break

    else:
        raise TypeError

    if not is_phase_1:
        return summits_list


def phase_1_simplex(solvable_matrix, min_b_value=0, max_iteration=100, prints=False):
    phase_1_matrix = np.zeros((len(solvable_matrix), len(solvable_matrix[-1]) + 1))
    phase_1_matrix[:-1, 0:-2] = solvable_matrix[:-1, 0: -1]
    phase_1_matrix[:-1, -2] = np.full(len(phase_1_matrix) - 1, -1)
    phase_1_matrix[-1, -2] = 1
    phase_1_matrix[:, -1] = solvable_matrix[:, -1]
    first_phase_1_pivot_line_index = np.where(phase_1_matrix[:, -1] == min_b_value)[0][0]
    first_phase_1_pivot_column_index = -2
    lets_pivot(phase_1_matrix, first_phase_1_pivot_line_index, first_phase_1_pivot_column_index)

    simplex_that_system(solvable_matrix=phase_1_matrix,
                        opt_max=False,
                        max_iteration=max_iteration,
                        is_phase_1=True,
                        prints=prints)

    solvable_matrix[:-1, :-1] = phase_1_matrix[:-1, :-2]
    solvable_matrix[:-1, -1] = phase_1_matrix[:-1, -1]
    phase_1_initial_base_indexes = find_base_indexes(phase_1_matrix)
    for line_index in phase_1_initial_base_indexes.keys():
        lets_pivot(solvable_matrix, line_index, phase_1_initial_base_indexes[line_index])

    print("end of phase 1, solvable matrix is now : \n", solvable_matrix, "\n")


def two_phases_simplex(solvable_matrix, opt_max=True, max_iteration=100, prints=False):
    assert isinstance(solvable_matrix, (np.ndarray, np.generic))
    solvable_matrix = solvable_matrix.astype(np.float64)
    print("with solvable matrix : \n", solvable_matrix, "\n")

    min_b_value = np.amin(solvable_matrix[0:-1, -1])
    if min_b_value < 0:
        phase_1_simplex(solvable_matrix, min_b_value, max_iteration, prints)

    print("solvable matrix is now : \n", solvable_matrix, "\n")

    return simplex_that_system(
        solvable_matrix=solvable_matrix,
        opt_max=opt_max,
        max_iteration=max_iteration,
        prints=prints)
