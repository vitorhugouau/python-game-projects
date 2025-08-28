import turtle
from random import randint

t = turtle.Turtle()
t.speed(0)
turtle.colormode(255)

for i in range(100):
    t.pencolor(randint(0, 255), randint(0, 255), randint(0, 255))
    t.forward(i * 5)
    t.right(30)

turtle.done()
