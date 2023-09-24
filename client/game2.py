# Import required library
import turtle
import random


class Pong():
    def __init__(self, left_pad, right_pad, sc):
        super().__init__()
        self.sc = sc
        self.sc.title("Pong game")
        self.sc.bgcolor("black")
        self.sc.setup(width=1000, height=600)

        # Draw a border around the Screen
        border = turtle.Turtle()
        border.speed(0)
        border.color("white")
        border.penup()
        border.setposition(-500, -300)
        border.pendown()
        border.pensize(3)
        for side in range(2):
            border.fd(1000)
            border.lt(90)
            border.fd(600)
            border.lt(90)
        border.hideturtle()

        self.sketch = turtle.Turtle()
        self.sketch.speed(0)
        self.sketch.color("white")
        self.sketch.penup()
        self.sketch.hideturtle()
        self.sketch.goto(0, 260)

        # Initialize score
        self.left_player_score = 0
        self.right_player_score = 0

    def update_score(self):
        self.sketch.clear()
        self.sketch.write("{}                {}".format(
            self.left_player_score,
            self.right_player_score
        ),
            align="center",
            font=("Courier", 24, "bold"))

    # Methods to update score
    def left_player_score_up(self):
        self.left_player_score += 1
        self.update_score()

    def right_player_score_up(self):
        self.right_player_score += 1
        self.update_score()


class Paddle(turtle.Turtle):
    def __init__(self, y_position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(5, 1)
        self.penup()
        self.goto(y_position, 0)

    def up(self):
        if self.ycor() < 225:
            y = self.ycor()
            y += 20
            self.sety(y)

    def down(self):
        if self.ycor() > -225:
            y = self.ycor()
            y -= 20
            self.sety(y)


class Ball(turtle.Turtle):
    def __init__(self, left_pad, right_pad):
        super().__init__()
        self.shape("circle")
        self.speed(40)
        self.color("white")
        self.penup()
        self.dx = 5 * random.choice((1, -1))
        self.dy = 5 * random.choice((1, -1))

    # Reset ball position
    def reset(self):
        self.goto(0, 0)
        self.dy *= -1


left_pad = Paddle(-400)
right_pad = Paddle(400)
hit_ball = Ball(left_pad, right_pad)
sc = turtle.Screen()
pong = Pong(left_pad, right_pad, sc)

# Keyboard bindings
sc.listen()
sc.onkeypress(left_pad.up, "w")
sc.onkeypress(left_pad.down, "s")
sc.onkeypress(right_pad.up, "Up")
sc.onkeypress(right_pad.down, "Down")
pong.update_score()

while True:
    sc.update()

    hit_ball.setx(hit_ball.xcor()+hit_ball.dx)
    hit_ball.sety(hit_ball.ycor()+hit_ball.dy)

    # Checking borders
    if hit_ball.ycor() > 280:
        hit_ball.sety(280)
        hit_ball.dy *= -1

    if hit_ball.ycor() < -280:
        hit_ball.sety(-280)
        hit_ball.dy *= -1

    if hit_ball.xcor() > 500:
        hit_ball.reset()
        pong.left_player_score_up()
        pong.update_score()

    if hit_ball.xcor() < -500:
        hit_ball.reset()
        pong.right_player_score_up()
        pong.update_score()

    # Paddle ball collision
    if (hit_ball.xcor() > 380 and hit_ball.xcor() < 420) and (hit_ball.ycor() < right_pad.ycor()+55 and hit_ball.ycor() > right_pad.ycor()-55):
        hit_ball.setx(380)
        hit_ball.dx *= -1

    if (hit_ball.xcor() < -380 and hit_ball.xcor() > -420) and (hit_ball.ycor() < left_pad.ycor()+55 and hit_ball.ycor() > left_pad.ycor()-55):
        hit_ball.setx(-380)

        hit_ball.dx *= -1
