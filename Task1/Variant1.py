from random import randint
rowcol=int(input('Size of matrix'))
un_null_row=0
max=0
zero_number = False
array = [[0 for i in range(rowcol)] for j in range(rowcol)]
for i in range(rowcol):
    for j in range(rowcol):
       array[i][j]=randint(-10,10)

for i in range(rowcol):
    for j in range(rowcol):
        print(array[i][j], end = ' ')
    print()

for i in range(rowcol):
    for j in range(rowcol):
        if array[i][j] == 0:
           zero_number = True
    if zero_number == False:
        un_null_row += 1
    zero_number = False

print('Ne nulovux',un_null_row)

max=array[0][0]
for i in range(rowcol):
    for j in range(rowcol):
        if array[i][j]>max:
            if array[i][j]==array[i][j]:
                max=array[i][j]

print('max number ',max)
