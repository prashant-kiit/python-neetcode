# Logical Operators

k = int(input('Enter the target: '))
n, m = 5, 10

smaller = n if n < m else m
bigger = n + m - smaller

if k < smaller:
    print("Very Less")
elif k > bigger:
    print('Very More')
elif k > smaller and k < bigger:
    print('Very Moderate')
else:
    print('On border line')
    
