from random import randint
row = 3
col = 4
array = [0] * row
for i in range(row):
    array[i] = [0] * col

for i in range(row):
    for j in range(col):
       array[i][j]=randint(-10,10)

for i in range(row):
    for j in range(col):
        print(array[i][j], end=' ')
    print()

neg = 0
negative = False
for i in range(row):
    for j in range(col):
        if array[i][j] < 0:
            neg += 1
        if array[i][j] == 0:
            negative = True
    if negative:
        print('in row ', i + 1, ': ', neg, ' negative elements\n')
    else:
        print('Vidsutni\n')
        neg = 0
        negative = False

for i in range(row):
    for j in range(col):
        negative = True
        for k in range(row):
            if array[i][j] > array[i][k]:
                negative = False
                break
        for b in range(col,negative):
            if array[i][j] < array[b][j]:
                negative = False
                break
        if negative:
            print('Row = ',i, ' ','Col = ', j)