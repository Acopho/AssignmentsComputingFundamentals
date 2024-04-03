
def quick_ksort(A, p, r, k):
    if abs(r - p) > k:
        q = partition(A, p, r)
        quick_ksort(A, p, q - 1, k) # inclusive ranges
        quick_ksort(A, q + 1, r, k)

def partition(A, p, r):
    x = A[r - 1]
    #print(f'partitioning range {p} to {r}')
    #print(f'pivot is {x}')
    i = p - 1
    for j in range(p, r):
        if A[j - 1] <= x:
            i += 1
            # Exchange A[i - 1] with A[j]
            if i - 1 < 0:
                continue
            #print(f'exchanging {i - 1} with {j} 0 indexed')
            aux1 = A[i - 1]
            A[i - 1] = A[j - 1]
            A[j - 1] = aux1
    # Exchange A[i] with A[j - 1]
    aux2 = A[i]
    A[i] = A[r - 1]
    A[r - 1] = aux2
    #print(f'partition from {p} to {r} is {A}')

    return i + 1

print('---------------------------------------------------')
k = 5
A = [4, 7, 5, 8, 0, 1, 2, 9, 3, 6]
print(f'k-sorting for array {A} with k {k}')
quick_ksort(A, 1, 10, k)
print('result')
print(A)
print('---------------------------------------------------')