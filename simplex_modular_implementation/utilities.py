from numpy import set_printoptions

set_printoptions(formatter={'float': lambda x: "{0:0.1f}".format(x)}, suppress=True)


def print_infos_on_simplex_run(summit_list_and_z_values):
    for index in range(len(summit_list_and_z_values[0])):
        print("vector X is : ", summit_list_and_z_values[0][index],
              " with value: ", summit_list_and_z_values[1][index], "\n")