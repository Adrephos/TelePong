import pygame

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (63, 12, 107)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 30


class Striker:
    # Take the initial position, dimensions, speed and color of the object
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect that is used to control the position and collision of the object
        self.playerRect = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the screen
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    # Used to display the object on the screen
    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.playerRect)

    def update(self, yFac):
        self.posy = self.posy + self.speed*yFac

        # Restricting the striker to be below the top surface of the screen
        if self.posy <= 0:
            self.posy = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT-self.height

        # Updating the rect with the new values
        self.playerRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text+str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.playerRect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed*self.xFac
        self.posy += self.speed*self.yFac

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and
        # it results in a reflection
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.firstTime = 1

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball

# Game Manager
def main():
    running = True

    # Defining the objects
    player1 = Striker(20, HEIGHT//2 - 50, 10, 100, 10, PURPLE)
    player2 = Striker(WIDTH-30, HEIGHT//2 - 50, 10, 100, 10, PURPLE)
    ball = Ball(WIDTH//2, HEIGHT//2, 7, 7, PURPLE)

    listOfPlayers = [player1, player2]

    # Initial parameters of the players
    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                #player 1 controls
                if event.key == pygame.K_w:
                    player1YFac = -1
                if event.key == pygame.K_s:
                    player1YFac = 1
                #player 2 controls
                if event.key == pygame.K_UP:
                    player2YFac = -1
                if event.key == pygame.K_DOWN:
                    player2YFac = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1YFac = 0

        # Collision detection
        for player in listOfPlayers:
            if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                ball.hit()

        # Updating the objects
        player1.update(player1YFac)
        player2.update(player2YFac)
        point = ball.update()

        # -1 -> Player_1 has scored
        # +1 -> Player_2 has scored
        # 0 -> None of them scored
        if point == -1:
            player1Score += 1
        elif point == 1:
            player2Score += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset it's position
        if point:
            ball.reset()

        # Displaying the objects on the screen
        player1.display()
        player2.display()
        ball.display()

        # Displaying the scores of the players
        player1.displayScore("Player_1 : ",
                           player1Score, 100, 20, PURPLE)
        player2.displayScore("Player_2 : ",
                           player2Score, WIDTH-100, 20, PURPLE)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
