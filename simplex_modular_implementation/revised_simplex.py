from numpy import array, where, amin, amax, divide, subtract, \
    hstack, vstack, identity, zeros, ndarray, generic, full, float64, \
    count_nonzero, delete, set_printoptions

set_printoptions(suppress=True)


def create_solvable_matrix(A, b, c):
    assert isinstance(A, (ndarray, generic))
    assert isinstance(b, (ndarray, generic))
    assert isinstance(c, (ndarray, generic))

    I = identity(len(A))
    zeros_vector = zeros(len(I))
    c = hstack([c, zeros_vector])

    solvable_matrix = hstack([A, I])
    solvable_matrix = vstack([solvable_matrix, array([c])])
    b = array([hstack([b, [array(0)]])]).T

    return float64(hstack([solvable_matrix, b]))


def is_phase_1_needed(solvable_matrix):
    if amin(solvable_matrix[:-1, -1]) < 0:
        return True
    return False


def create_phase_1_matrix(solvable_matrix):
    number_of_lines = len(solvable_matrix) + 1
    number_of_columns = len(solvable_matrix[-1]) + 1
    negative_one_vector = full(number_of_lines-2, -1).T
    phase_1_matrix = zeros([number_of_lines, number_of_columns])
    phase_1_matrix[:number_of_lines-2, :number_of_columns-2] = solvable_matrix[:-1, :-1]
    phase_1_matrix[:-2, -2] = negative_one_vector
    phase_1_matrix[-2, -2] = 1
    phase_1_matrix[:-2, -1] = solvable_matrix[:-1, -1]
    phase_1_matrix[-1, :number_of_columns-1] = solvable_matrix[-1]

    return phase_1_matrix


def find_possible_column_index(solvable_matrix, opt_max=True, is_phase_1=False):
    line_index = -1
    if is_phase_1:
        line_index = -2

    possibility_vector = solvable_matrix[line_index, :-1]
    if opt_max:
        maximum = amax(possibility_vector)
        if maximum > 0.00000000001:
            return array(where(possibility_vector == maximum)[0])
    else:
        minimum = amin(possibility_vector)
        if minimum < -0.00000000001:
            return array(where(possibility_vector == minimum)[0])


def find_possible_line_index(solvable_matrix, possible_column_indexes, is_phase_1=False):
    possible_line_indexes = list()

    line_index = -1
    if is_phase_1:
        line_index = -2

    for column_index in possible_column_indexes:
        numerators = solvable_matrix[:line_index, -1]
        denominators = solvable_matrix[:line_index, column_index]

        indexes_of_zeros = where(denominators == 0)[0]

        for index in indexes_of_zeros:
            if numerators[index] < 0:
                denominators[index] = -0.000000000001
            else:
                denominators[index] = 0.000000000001

        selection_values = divide(numerators, denominators)
        value = amin(selection_values[selection_values > 0])
        possible_line_index = where(selection_values == value)[0][0]
        possible_line_indexes.append([possible_line_index, value])

    return array(possible_line_indexes)


def find_line_and_column_index_for_pivot(possible_column_indexes, possible_line_indexes):
    assert len(possible_column_indexes) == len(possible_column_indexes)

    true_line_value = amin(possible_line_indexes[:, 1])
    minimal_value_index = where(possible_line_indexes[:, -1] == true_line_value)[0][0]
    column_index = possible_column_indexes[minimal_value_index]
    line_index = possible_line_indexes[minimal_value_index, 0]

    return array([line_index, column_index])


def pivot_around_value(solvable_matrix, pivot_index):
    line_index = int(pivot_index[0])
    column_index = int(pivot_index[1])

    solvable_matrix[line_index] = solvable_matrix[line_index]/solvable_matrix[line_index, column_index]

    for i in range(len(solvable_matrix)):
        if i != line_index and solvable_matrix[i, column_index] != 0:
            coefficient = solvable_matrix[i, column_index]/solvable_matrix[line_index, column_index]
            solvable_matrix[i] = subtract(solvable_matrix[i], coefficient*solvable_matrix[line_index])


def phase_1_special_pivot(phase_1_matrix):
    column_index = array([-2])
    line_index = where(phase_1_matrix[:-1, -1] == amin(phase_1_matrix[:-1, -1]))
    pivot_index = array([line_index, column_index])
    pivot_around_value(phase_1_matrix, pivot_index)


def simplex_all_steps_for_1_iteration(solvable_matrix, opt_max=True, is_phase_1=False):
    column_possible_indexes = find_possible_column_index(solvable_matrix, opt_max, is_phase_1)
    line_possible_indexes_and_values = find_possible_line_index(solvable_matrix, column_possible_indexes, is_phase_1)

    pivot_index = find_line_and_column_index_for_pivot(
        possible_column_indexes=column_possible_indexes,
        possible_line_indexes=line_possible_indexes_and_values)

    pivot_around_value(solvable_matrix, pivot_index)


def is_max(solvable_matrix, is_phase_1=False):
    line_index = -1
    if is_phase_1:
        line_index = -2
    if amax(solvable_matrix[line_index, :-1]) <= 1.0E-10:
        return True
    return False


def is_min(solvable_matrix, is_phase_1=False):
    line_index = -1
    if is_phase_1:
        line_index = -2
    if amin(solvable_matrix[line_index, :-1]) >= -1.0E-10:
        return True
    return False


def find_base_indexes(solvable_matrix):
    indexes = dict()
    for column_index in range(len(solvable_matrix[-1]) - 1):
        if count_nonzero(solvable_matrix[:, column_index] == 1.0) ==1 and \
                (count_nonzero(solvable_matrix[:, column_index] == 0.0)) == len(solvable_matrix[:, column_index]) -1:
            indexes[where(solvable_matrix[:, column_index] == 1)[0][0]] = column_index
    return indexes


def from_base_indexes_find_solution_vector(solvable_matrix, current_base_indexes):
    assert isinstance(current_base_indexes, dict)
    summit = zeros(len(solvable_matrix.T) - 1)
    for line_index in current_base_indexes.keys():
        summit[current_base_indexes[line_index]] = solvable_matrix[line_index, -1]
    return summit


def phase_2_algorithm(solvable_matrix, opt_max=True, max_iter=10000, is_phase_1=False):
    summit_list = list()
    values = list()

    if not is_phase_1:
        print("starting phase 2 \n")

    if opt_max:
        for i in range(max_iter):
            if is_max(solvable_matrix, is_phase_1):
                print("reached_max")
                break
            else:
                simplex_all_steps_for_1_iteration(solvable_matrix, opt_max, is_phase_1=is_phase_1)
                if not is_phase_1:
                    base_indexes = find_base_indexes(solvable_matrix)
                    summit_list.append(from_base_indexes_find_solution_vector(solvable_matrix, base_indexes))
                    values.append(-1*solvable_matrix[-1, -1])

    elif not opt_max:
        for i in range(max_iter):
            if is_min(solvable_matrix, is_phase_1):
                print("reached_min")
                break
            else:
                simplex_all_steps_for_1_iteration(solvable_matrix, opt_max, is_phase_1=is_phase_1)
                if not is_phase_1:
                    base_indexes = find_base_indexes(solvable_matrix)
                    summit_list.append(from_base_indexes_find_solution_vector(solvable_matrix, base_indexes))
                    values.append(-1*solvable_matrix[-1, -1])

    else:
        print("enter better inputs")

    if not is_phase_1:
        return summit_list, values


def phase_1_algorithm(solvable_matrix, max_iterations=10000):
    phase_1_matrix = create_phase_1_matrix(solvable_matrix)
    phase_1_special_pivot(phase_1_matrix)
    phase_2_algorithm(phase_1_matrix, opt_max=False, max_iter=max_iterations, is_phase_1=True)
    phase_1_matrix = delete(phase_1_matrix, -2, 1)
    phase_1_matrix = delete(phase_1_matrix, -2, 0)
    return phase_1_matrix


def format_summit_list(summit_list, len_x):
    new_summit_list = list()
    for i in range(len(summit_list[0])):
        new_summit_list.append(summit_list[0][i][:len_x])
    return new_summit_list, summit_list[1]


def two_phase_simplex(solvable_matrix, opt_max=True, max_iter=10000, len_x=0):
    assert isinstance(solvable_matrix, (ndarray, generic))
    if len_x == 0:
        len_x = len(solvable_matrix) + 1

    print("does need phase 1? ", is_phase_1_needed(solvable_matrix))

    if is_phase_1_needed(solvable_matrix):
        solvable_matrix = phase_1_algorithm(solvable_matrix, max_iterations=max_iter)
    summit_list = phase_2_algorithm(solvable_matrix, opt_max, max_iter)

    return format_summit_list(summit_list, len_x)
