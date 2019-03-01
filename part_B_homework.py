from numpy import array, multiply, sum, identity, vstack, hstack, ones, zeros
from simplex_modular_implementation.revised_simplex import two_phase_simplex, create_solvable_matrix
from simplex_modular_implementation.utilities import print_infos_on_simplex_run

# probleme diete
cost_array = array([1.84, 2.19, 1.84, 1.44, 2.29, 0.77, 1.29, 0.60, 0.72])
c = array([1.84, 2.19, 1.84, 1.44, 2.29, 0.77, 1.29, 0.60, 0.72])  # function objective

# les donnees
cal = array([510, 370, 500, 370, 400, 220, 345, 110, 80])
carbo = array([34, 35, 42, 38, 42, 26, 27, 12, 20])
protein = array([28, 24, 25, 14, 31, 3, 15, 9, 1])
vitA = array([15, 15, 6, 2, 8, 0, 4, 10, 2])
vitC = array([6, 10, 2, 0, 15, 15, 0, 4, 120])
calc = array([30, 20, 25, 15, 15, 0, 20, 30, 2])
fer = array([20, 20, 20, 10, 8, 2, 15, 0, 2])

Seuil=-1*array([2000, 350, 55, 100, 100, 100, 100])

A = -1*array([
    cal,
    carbo,
    protein,
    vitA,
    vitC,
    calc,
    fer
])


aliments = {
    0: "Quart de livre from",
    1: "Hamburg deluxe from",
    2: "BigMac",
    3: "Filet poisson",
    4: "Mac Poulet",
    5: "Frites",
    6: "Saucisses McMuffin",
    7: "Lait",
    8: "Jus orange",
}


print("part B of homework \n "
      "_____________________________________________________________________________________________ \n"
      "    number 1)    \n")
solvable_matrix = create_solvable_matrix(A=A, b=Seuil, c=c)
summits = two_phase_simplex(solvable_matrix, opt_max=False)
#print_infos_on_simplex_run(summits)

print("aliments bougth for ", summits[1][-1], " are: \n")
for i in range(len(summits[0][-1])):
    print("    ", summits[0][-1][i], " ", aliments[i], "\n")

x = summits[0][-1]

total_cal = sum(multiply(cal, x))
print("with ", total_cal, " calories for the day")

print("_____________________________________________________________________________________________ \n"
      "    number 2)    \n")

A = -1*array([
    cal,
    -cal,
    carbo,
    protein,
    vitA,
    vitC,
    calc,
    fer
])

b = -1*array([2000, -2500, 350, 55, 100, 100, 100, 100])

c=array([1.84, 2.19, 1.84, 1.44, 2.29, 0.77, 1.29, 0.60, 0.72])

solvable_matrix = create_solvable_matrix(A=A, b=b, c=c)
summits = two_phase_simplex(solvable_matrix, opt_max=False)
#print_infos_on_simplex_run(summits)

print("aliments bougth for ", summits[1][-1], " are: \n")
for i in range(len(summits[0][-1][:-1])):
    print("    ", summits[0][-1][i], " ", aliments[i], "\n")

x = summits[0][-1][:-1]

total_cal = sum(multiply(cal, x))
print("with ", total_cal, " calories for the day")

print("_____________________________________________________________________________________________ \n"
      "    number 3)    \n")

b = -1*array([2000, -2000, 350, 55, 100, 100, 100, 100])

solvable_matrix = create_solvable_matrix(A=A, b=b, c=c)
summits = two_phase_simplex(solvable_matrix, opt_max=False)
print_infos_on_simplex_run(summits)

print("Seems like not")

print("_____________________________________________________________________________________________ \n"
      "    number 4)    \n")

A = -1*array([
    carbo,
    protein,
    vitA,
    vitC,
    calc,
    fer
])

b = -1*array([350, 55, 100, 100, 100, 100])

c = cal

solvable_matrix = create_solvable_matrix(A=A, b=b, c=c)
summits = two_phase_simplex(solvable_matrix, opt_max=False, len_x=9)
#print_infos_on_simplex_run(summits)

x = summits[0][-1]
total_cost = sum(multiply(cost_array, x))

print("minimal calories for diet are : ", summits[1][-1], ", for a total cost of : ", total_cost)

print("_____________________________________________________________________________________________ \n"
      "    number 5)    \n")

new_constraints = identity(len(cost_array))
new_constraints_ubound = -2 * ones(len(new_constraints))
new_constraints_lbound = zeros(len(new_constraints))

A = -1*array([
    cal,
    carbo,
    protein,
    vitA,
    vitC,
    calc,
    fer

])

A = vstack([A, new_constraints, -new_constraints])


b = -1*hstack([array([2000, 350, 55, 100, 100, 100, 100]), new_constraints_ubound, new_constraints_lbound])
c = cost_array

solvable_matrix = create_solvable_matrix(A=A, b=b, c=c)
summits = two_phase_simplex(solvable_matrix, opt_max=False, len_x=9)
#print_infos_on_simplex_run(summits)

x = summits[0][-1]
total_cal = sum(multiply(cal, x))

print("for a minimal cost of ", summits[1][-1], " total calories are ", total_cal, "\n")
