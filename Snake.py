import random
import turtle
import time


direction = "right"
segments = []

def grow_snake():
    segment = turtle.Turtle()
    segment.shape("square")
    segment.color("white")
    segment.turtlesize(1.5,1.5)
    segment.penup()
    segment.speed(0)

    if len(segments) == 0:
        segment.goto(pen.xcor(), pen.ycor())
    else:
        segment.goto(segments[-1].xcor(), segments[-1].ycor())

    segments.append(segment)


def go_up():
    global direction
    pen.setheading(90)
    if direction != "down":
        direction = "up"


def go_down():
    global direction
    pen.setheading(270)
    if direction != "up":
        direction = "down"

def go_left():
    global direction
    pen.setheading(180)
    if direction != "right":
        direction = "left"

def go_right():
    global direction
    pen.setheading(0)
    if direction != "left":
        direction = "right"

def draw_grid():
    grid_size = 50

    turtle = pen.clone()
    turtle.color("grey")
    turtle.speed(0)
    turtle.penup()

    # vertical lines
    for x in range(-300, 301, grid_size):
        turtle.goto(x, -300)
        turtle.pendown()
        turtle.goto(x, 300)
        turtle.penup()

    # horizontal lines
    for y in range(-300, 301, grid_size):
        turtle.goto(-300, y)
        turtle.pendown()
        turtle.goto(300, y)
        turtle.penup()

    turtle.hideturtle()

def spawn_apple():
    x = random.randint(-13, 13) * 20
    y = random.randint(-13, 13) * 20

    apple.goto(x, y)


def game_loop():
    
    growth_rate = 2

    global game_running
    pen.penup()
    while game_running:

        x = pen.xcor()
        y = pen.ycor()

        if x > 267 or x < -275 or y > 277 or y < -271:
            game_running = False

        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)

        if direction == "up":
            pen.setheading(90)
        elif direction == "down":
            pen.setheading(270)
        elif direction == "left":
            pen.setheading(180)
        elif direction == "right":
            pen.setheading(0)

        if len(segments) > 0:
            segments[0].goto(pen.xcor(), pen.ycor())


        pen.forward(3)

        screen.update()
        time.sleep(0.01)

        if pen.distance(apple) < 20:
            spawn_apple()
            for i in range(growth_rate):
                grow_snake()
        
    


screen = turtle.Screen()
screen.setup(600, 600)
screen.title("Snake")
screen.bgcolor("black")
screen.tracer(0)

pen = turtle.Turtle()
pen.color("white")
pen.shape("arrow")
pen.speed(0)
pen.turtlesize(3,3)

apple = turtle.Turtle()
apple.shape("circle")
apple.color('red')
apple.penup()
apple.speed(0)
apple.turtlesize(2,2)


game_running = True

screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

screen.listen()

draw_grid()
screen.update()
pen.penup()
pen.goto(-50,25)
pen.pendown()
game_loop()

turtle.done()