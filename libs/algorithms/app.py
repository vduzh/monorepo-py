import math

# start of the task
n, k = [int(s) for s in input("").split()]

num_of_rows = math.comb(n, k)
num_of_cells = math.comb(n, k)
num_of_permutations = math.perm(k, k)

res = num_of_rows * num_of_cells * num_of_permutations

print(res)

# end of the task
