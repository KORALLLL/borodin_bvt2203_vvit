print('Введите коэффициенты a,b,c')
a, b, c = int(input()), int(input()), int(input())
d = (b * b - 4 * a * c)

if a == 0 and b == 0 and c!=0:
    print("it doesn't has roots")
elif a == 0 and b == 0 and c == 0 :
    print('any number is a root')
else:
    if a==0:
        print(c/b)
    else:
        if d<0:
            print("it doesn't has real roots")
        else:
            x1 = (-b-d**0.5)/2/a
            x2 = (-b+d**0.5)/2/a
            print(x1,x2)
