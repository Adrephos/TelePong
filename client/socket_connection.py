import socket
import constants
import keyboard
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

this_player_paddle = 0
other_player_paddle = 0
ball_x = 0
ball_y = 0
ball_speed_x = 0
ball_speed_y = 0
player_score = 0
other_player_score = 0
ball_speed = 0

print('***********************************')
print('Client is running...')
print('client_socket:', client_socket)
client_socket.connect((constants.IP_SERVER, constants.PORT))
local_tuple = client_socket.getsockname()
print('Connected to the server from:', local_tuple)
print('Enter \"quit\" to exit')


def parse_data(data):
    data = data.split(' ')
    return data


def send_msg(msgType, payload=''):
    command = msgType + ' ' + payload

    client_socket.send(
        bytes(command, constants.ENCONDING_FORMAT))

    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)

    return data_received.decode(constants.ENCONDING_FORMAT)


def read_msg():
    data_received = ""
    data_received = data_received.encode(constants.ENCONDING_FORMAT)
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
    return data_received.decode(constants.ENCONDING_FORMAT)


def get_state():
    state = str(this_player_paddle) + ' ' + str(ball_x) + ' ' + str(
        ball_y) + ' ' + str(ball_speed_x) + ' ' + str(
        ball_speed_y) + ' ' + str(ball_speed)
    return state


def set_state(state):
    global other_player_paddle
    other_player_paddle = int(state[1])
    global ball_x
    ball_x = int(state[2])
    global ball_y
    ball_y = int(state[3])
    global ball_speed_x
    ball_speed_x = int(state[4])
    global ball_speed_y
    ball_speed_y = int(state[5])
    global ball_speed
    ball_speed = int(state[6])


def request_state():
    data_received = send_msg(constants.GET_STATE)
    if parse_data(data_received)[0] == constants.POST_STATE:
        set_state(parse_data(data_received))
    print(data_received)


# Player registration
nickname = input('Nickname: ')
send_msg(constants.REGISTER, nickname)
player_number = 0

# Create or join a room
create = 'na'
while create != 'c' and create != 'j':
    create = input('Create or join a room? c/j: ')

if create == 'c':
    game_id = send_msg(constants.CREATE)
    print("Room id: ", game_id.split(' ')[1])
    print('Waiting for another player to join...')
    data_received = read_msg()
    if parse_data(data_received)[0] == constants.START:
        player_number = 1
        print('Game started!')
elif create == 'j':
    error = True
    while error:
        game_id = input('Room id: ')
        data_received = send_msg(constants.JOIN, game_id)
        if data_received.split(' ')[0] == constants.ERR:
            print(data_received[len(constants.ERR)+1:])
        else:
            error = False
            print('Game started!')
            player_number = 2


# Simulate game loop
i = 0
print(player_number)
while True:
    if i != 0:
        state = request_state()
    if player_number == 1 and i == 0:
        i += 1
        data_received = send_msg(constants.POST_STATE, get_state())
    else:
        # In linux you need to run the script as root to use keyboard
        if keyboard.is_pressed('w'):
            if i == 0:
                i += 1
            this_player_paddle += 1
            data_received = send_msg(constants.POST_STATE, get_state())
    time.sleep(0.2)

client_socket.close()
