import tpp
import sys
import pygame
import constants
import threading
import pygame_gui
import time
import re


pygame.init()

# RGB values of standard colors
BLACK = (27, 36, 48)
GRAY = (81, 85, 126)
PURPLE = (129, 103, 151)
YELLOW = (214, 213, 168)
WHITE = (196, 196, 196)
RED = (201, 44, 109)

FONT = "assets/UpheavalPro.ttf"


# Basic parameters of the screen
WIDTH, HEIGHT = 1280, 720
BG = pygame.image.load("assets/Background.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

text_input_width = 400
text_input_height = 50
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
manager_join = pygame_gui.UIManager((WIDTH, HEIGHT))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH//2-(text_input_width//2), 250), (text_input_width, text_input_height)),
                                                 manager=manager, object_id='#main_text_entry')

text_email = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH//2-(text_input_width//2), (HEIGHT//2)+50), (text_input_width, text_input_height)),
                                                 manager=manager, object_id='#email_text_entry')

room_id_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH//2-(text_input_width//2), (HEIGHT//2)), (text_input_width, text_input_height)),
                                                    manager=manager_join, object_id='#id_text_entry')

clock = pygame.time.Clock()
FPS = 30


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)


# Striker class
class Striker:
    # Take the initial position, dimensions, speed and color of the object
    def __init__(self, posx, posy, width, height, speed, color, nickname):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.nickname = nickname
        # Rect that is used to control the position and collision of the object
        self.geekRect = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the screen
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    # Used to display the object on the screen
    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy = self.posy + self.speed*yFac

        # Restricting the striker to be below the top surface of the screen
        if self.posy <= 0:
            self.posy = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT-self.height

        # Updating the rect with the new values
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def setPos(self, posy):
        self.posy = posy
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        font = get_font(60)
        score = font.render(str(score), True, color)
        textRect = score.get_rect()
        textRect.center = (x, y+20)

        font2 = get_font(20)
        player_name = font2.render(str(text), True, color)
        textRect2 = player_name.get_rect()
        textRect2.center = (x, HEIGHT-y)

        screen.blit(score, textRect)
        screen.blit(player_name, textRect2)

    def getRect(self):
        return self.geekRect


# Ball class
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

    def setPos(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def setSpeed(self, speed, xFac, yFac):
        self.speed = speed
        self.xFac = xFac
        self.yFac = yFac

    def getInfo(self):
        # Returns x and y coords, speed, xFac and yFac as str and with 2 decimal places
        return [str(round(self.posx, 2)), str(round(self.posy, 2)),
                str(round(self.xFac, 2)), str(round(self.yFac, 2)),
                str(round(self.speed, 2))
                ]

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
        self.xFac *= -1
        self.firstTime = 1

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.speed += 0.2
        self.xFac *= -1

    def getRect(self):
        return self.ball


class UpdateThread(threading.Thread):
    def __init__(self, protocol: tpp.Tpp, other_player, ball):
        threading.Thread.__init__(self, daemon=True)
        self.protocol = protocol
        self.other_player = other_player
        self.ball = ball

    def update(self, other_player, ball):
            received_state = self.protocol.read_msg()
            parsed_data = self.protocol.parse_data(received_state)
            if parsed_data[0] == constants.POST_STATE:
                paddle = float(parsed_data[1])
                ball_x = float(parsed_data[2])
                ball_y = float(parsed_data[3])
                ball_speed_x = float(parsed_data[4])
                ball_speed_y = float(parsed_data[5])
                ball_speed = float(re.findall(r"[-+]?[0-9]*\.?[0-9]+", parsed_data[6])[0])

                self.ball.setPos(ball_x, ball_y)
                self.ball.setSpeed(ball_speed, ball_speed_x, ball_speed_y)
                self.other_player.setPos(paddle)

    def run(self):
        while True:
            self.update(self.other_player, self.ball)


# Game Manager
def play(protocol, this_name, other_name, this_number):
    running = True

    # Defining the objects
    if this_number == 1:
        this_player = Striker(20, 0, 20, 120, 15, GRAY, this_name)
        other_player = Striker(WIDTH-40, 0, 20, 120, 17, GRAY, other_name)
    else:
        this_player = Striker(WIDTH-30, 0, 20, 120, 15, GRAY, this_name)
        other_player = Striker(20, 0, 20, 120, 17, GRAY, other_name)

    ball = Ball(WIDTH//2, HEIGHT//2, 7, 10, YELLOW)

    listOfPlayers = [this_player, other_player]

    # Initial parameters of the players
    this_playerScore, other_playerScore = 0, 0
    this_playerFac = 0
    update = False

    # Thread to update the game received_state
    thread = UpdateThread(protocol, other_player, ball)
    UpdateThread.update(thread, other_player, ball)
    thread.start()

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    update = True
                    this_playerFac = -1
                if event.key == pygame.K_s:
                    update = True
                    this_playerFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    update = False
                    this_playerFac = 0

        # Collision detection
        for geek in listOfPlayers:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()

        # Updating the objects
        this_player.update(this_playerFac)
        point = ball.update()
        if update:
            state = f'{round(this_player.posy, 2)} {round(ball.posx, 2)} {round(ball.posy, 2)} {round(ball.xFac, 2)} {round(ball.yFac, 2)} {round(ball.speed, 2)}'
            protocol.send_msg(constants.POST_STATE, state)

        if point == -1:
            if this_number == 1:
                this_playerScore += 1
            elif this_number == 2:
                other_playerScore += 1
        elif point == 1:
            if this_number == 2:
                this_playerScore += 1
            elif this_number == 1:
                other_playerScore += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset it's position
        if point:
            ball.reset()

        if this_playerScore == 5:
            running = False
            end_game(protocol, "YOU WIN!!!!", WHITE)
        elif other_playerScore == 5:
            running = False
            end_game(protocol, other_name + " WINS!!!!", RED)

        # Displaying the objects on the screen
        this_player.display()
        other_player.display()
        ball.display()

        # Displaying the scores of the players
        if this_number == 1:
            this_player.displayScore(this_player.nickname,
                                     this_playerScore, 400, 20, RED)
            other_player.displayScore(other_player.nickname,
                                      other_playerScore, WIDTH-400, 20, YELLOW)
        else:
            this_player.displayScore(this_player.nickname,
                                     this_playerScore, WIDTH-400, 20, RED)
            other_player.displayScore(other_player.nickname,
                                      other_playerScore, 400, 20, YELLOW)

        time.sleep(0.06)
        pygame.display.update()


def end_game(protocol: tpp.Tpp, text: str, color):
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(100).render(
            "TelePong", True, YELLOW)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        end_text = get_font(40).render(text, True, color)

        quit_game = Button(image=None, pos=(640, 600),
                           text_input="quit game", font=get_font(55), base_color=PURPLE, hovering_color=YELLOW)
        screen.blit(
            end_text, (WIDTH//2 - (end_text.get_width()//2), HEIGHT//2))

        for button in [quit_game]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_game.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(FONT, size)


# Thread to wait for players and show the room id
class WaitThread(threading.Thread):
    def __init__(self, protocol: tpp.Tpp, flag: bool):
        threading.Thread.__init__(self, daemon=True)
        self.protocol = protocol
        self.flag = flag
        self.other_name = ""

    def run(self):
        self.other_name = self.protocol.wait_for_player()
        self.flag = True


def waiting_for_game(protocol: tpp.Tpp, room_id: str, this_name: str):
    thread = WaitThread(protocol, False)
    thread.start()
    while True:
        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(100).render(
            "TelePong", True, YELLOW)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        room_text = get_font(30).render("ROOM ID", True, YELLOW)
        id_text = get_font(30).render(" "+str(room_id), True, WHITE)
        wait_text = get_font(40).render("Waiting for players...", True, PURPLE)

        screen.blit(room_text, (10, 10))
        screen.blit(id_text, (10, 40))
        screen.blit(
            wait_text, (WIDTH//2 - (wait_text.get_width()//2), HEIGHT//2))

        if thread.flag:
            play(protocol, this_name, thread.other_name, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def join_game_screen(protocol: tpp.Tpp, this_name: str):
    data, error = "", False
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000

        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        error_text = get_font(20).render(data, True, RED)

        menu_text = get_font(100).render("TelePong", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(640, 100))

        room_id_label = get_font(40).render("Room id", True, WHITE)

        submit_button = Button(image=None, pos=(640, 600),
                               text_input="Submit", font=get_font(55), base_color=PURPLE, hovering_color=WHITE)

        screen.blit(menu_text, menu_rect)
        screen.blit(error_text, (130 - error_text.get_width() // 2, HEIGHT-30))
        screen.blit(room_id_label, (640 - room_id_label.get_width() // 2, (HEIGHT//2)-50))

        for button in [submit_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.checkForInput(MENU_MOUSE_POS):
                    room_id = str(room_id_input.get_text())
                    data, error = protocol.join_room(room_id)
                    if error:
                        continue
                    else:
                        play(protocol, this_name, data, 2)

                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                        event.ui_object_id == '#id_text_entry'):
                    print(event.text)

            manager_join.process_events(event)

        manager_join.update(UI_REFRESH_RATE)
        manager_join.draw_ui(screen)
        pygame.display.update()


def game_lobby(protocol: tpp.Tpp, this_name: str):
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(100).render(
            "TelePong", True, YELLOW)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        create_game = Button(image=None, pos=(640, 320),
                             text_input="CREATE ROOM", font=get_font(55), base_color=PURPLE, hovering_color=YELLOW)
        join_game = Button(image=None, pos=(640, 520),
                           text_input="JOIN ROOM", font=get_font(55), base_color=PURPLE, hovering_color=YELLOW)

        for button in [create_game, join_game]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if create_game.checkForInput(OPTIONS_MOUSE_POS):
                    room_id = protocol.create_room()
                    waiting_for_game(protocol, room_id, this_name)
                if join_game.checkForInput(OPTIONS_MOUSE_POS):
                    join_game_screen(protocol, this_name)

        pygame.display.update()


def main_menu(protocol: tpp.Tpp):
    error = ""
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000

        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        error_text = get_font(20).render(error, True, RED)

        menu_text = get_font(100).render("TelePong", True, YELLOW)
        menu_rect = menu_text.get_rect(center=(640, 100))

        nickname_label = get_font(40).render("Nickname", True, WHITE)
        email_label = get_font(40).render("Email", True, WHITE)

        submit_button = Button(image=None, pos=(640, 600),
                               text_input="Submit", font=get_font(55), base_color=PURPLE, hovering_color=WHITE)

        screen.blit(menu_text, menu_rect)
        screen.blit(
            error_text, (130 - nickname_label.get_width() // 2, HEIGHT-30))
        screen.blit(nickname_label,
                    (640 - nickname_label.get_width() // 2, 200))
        screen.blit(
            email_label, (640 - email_label.get_width() // 2, HEIGHT//2))

        for button in [submit_button]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.checkForInput(MENU_MOUSE_POS):
                    username = str(text_input.get_text())
                    if username == "":
                        error = "Please enter a Nickname"
                        continue
                    protocol.register_player(username)
                    game_lobby(protocol, username)

                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                        event.ui_object_id == '#main_text_entry'):
                    print(event.text)
                    protocol.register_player(event.text)
            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(screen)
        pygame.display.update()


def main():
    protocol = tpp.Tpp(constants.IP_SERVER)
    protocol.connect_to_server()
    # play(protocol, "Player 1", "Player 2", 1)
    main_menu(protocol)


if __name__ == "__main__":
    main()
