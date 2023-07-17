from random import randint
rowcol=int(input('Size of matrix '))
proiz = 1
max = 0
negative = False
array=[[0 for i in range(rowcol)] for j in range(rowcol)]

for i in range(rowcol):
    for j in range(rowcol):
       array[i][j]=randint(-10,10)

for i in range(rowcol):
    for j in range(rowcol):
        print(array[i][j], end = ' ')
    print()

for i in range(rowcol):
    for j in range(rowcol):
        if array[i][j] < 0:
            negative = True
        proiz *= array[i][j]
    if negative == False:
        print('doputok elementiv ',proiz)
    negative = False
    proiz = 1

sum_diag = [0] * (rowcol - 1) * 2
for i in range(rowcol - 1):
    b = 0
    c = 0 + i
    for j in range(1 + i, rowcol):
        if j > rowcol:
            break
        sum_diag[i] += array[j][b]
        b += 1

    for k in range(rowcol):
        if k > rowcol - 1 - i:
            break
        sum_diag[i + rowcol - 1] += array[k][c]
        c += 1

max_sum = sum_diag[0]

for i in sum_diag:
    if i > max_sum:
        max_sum = i

print('Max summa diagonal ',max_sum)

