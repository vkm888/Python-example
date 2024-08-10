from turtle import *
s=0
pensize(10)
while True:
    forward(3)

    if s < 90:
        s=s+1
        left(1)
        print('90v1',s)
    elif  s > 360:
        s=s+1
        right(1)
        print('360',s)
    elif  s > 90:
        s=s+1
        right(1)
        print('90v2',s)
    else:
        s=s+1
        right(1)
        print('else',s)



# exitonclick()