import socket
import constants
import threading
# import time


class Tpp:
    def __init__(self, server_ip):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_number = 0
        self.this_player_paddle = 500
        self.other_player_paddle = 0
        self.ball_x = 0
        self.ball_y = 0
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.ball_speed = 0
        self.server_ip = server_ip

    def connect_to_server(self):
        print('***********************************')
        print('Client is running...')
        print('client_socket:', self.client_socket)
        print('***********************************')
        self.client_socket.connect((self.server_ip, constants.PORT))

    def parse_data(self, data):
        data = data.split(' ')
        return data

    def read_msg(self):
        data_received = ""
        data_received = data_received.encode(constants.ENCONDING_FORMAT)
        try:
            data_received = self.client_socket.recv(constants.RECV_BUFFER_SIZE)
        except BlockingIOError:
            pass
        return data_received.decode(constants.ENCONDING_FORMAT)

    def send_msg(self, msgType, payload=''):
        command = msgType + ' ' + payload
        self.client_socket.send(
            bytes(command, constants.ENCONDING_FORMAT))

    def actual_state(self):
        state = f'{self.this_player_paddle} {self.ball_x} {self.ball_y} ' \
                f'{self.ball_speed_x} {self.ball_speed_y} {self.ball_speed}'
        return state

    def set_state(self, state):
        self.other_player_paddle = int(state[1])
        self.ball_x = int(state[2])
        self.ball_y = int(state[3])
        self.ball_speed_x = int(state[4])
        self.ball_speed_y = int(state[5])
        self.ball_speed = int(state[6])

    def set_player_padle(self, paddle):
        self.this_player_paddle = paddle

    def register_player(self, nickname):
        self.send_msg(constants.REGISTER, nickname)
        data_received = self.read_msg()
        if self.parse_data(data_received)[0] == constants.SUCC:
            print('Registered successfully!')
        else:
            print('Error registering!')

    def create_room(self):
        self.send_msg(constants.CREATE)
        data_received = self.read_msg()
        parsed_data = self.parse_data(data_received)
        return parsed_data[1]  # game_id

    # Returns the user nickname of the other player
    def wait_for_player(self):
        data_received = self.read_msg()
        parsed_data = self.parse_data(data_received)
        if parsed_data[0] == constants.START:
            self.player_number = 1
            return parsed_data[1]

    # Returns the user nickname of the other player or an error message
    def join_room(self, game_id):
        self.send_msg(constants.JOIN, game_id)
        data_received = self.read_msg()
        parsed_data = self.parse_data(data_received)
        if parsed_data[0] == constants.ERR:
            return data_received[len(constants.ERR) + 1:], True
        elif parsed_data[0] == constants.SUCC:
            return parsed_data[1], False

    def receive_state(self):
        received_state = self.read_msg()
        parsed_data = self.parse_data(received_state)
        if parsed_data[0] == constants.POST_STATE:
            self.set_state(parsed_data)

    # Function that reads the socket constantly and updates the game state
    def update_game_state(self):
        while True:
            self.receive_state()

    def send_state(self):
        self.send_msg(constants.POST_STATE, self.actual_state())

    def initialize_game(self):
        # Player registration
        nickname = input('Nickname: ')
        self.register_player(nickname)

        nicknname_p2 = ''

        # Create or join a room
        create = 'na'
        while create != 'c' and create != 'j':
            create = input('Create or join a room? c/j: ')

        if create == 'c':
            room = self.create_room()
            print('Room created successfully! ID: ', room)
            nicknname_p2 = self.wait_for_player()
        elif create == 'j':
            data, error = "", True
            while error:
                game_id = input('Game ID: ')
                data, error = self.join_room(game_id)
                if error:
                    print(data)
                else:
                    nicknname_p2 = data
        print(nickname, ' vs ', nicknname_p2)
        # Receive initial game state
        self.receive_state()
        # create thread to update game state
        data_receiver_thread = threading.Thread(
            target=self.update_game_state, daemon=True)
        data_receiver_thread.start()

        # if key pressed, update paddle position and send it to server
        while True:
            if input('Press w to move paddle up: ') == 'w':
                self.this_player_paddle += 1
                self.send_state()

    def main_game_loop(self):
        print(self.player_number)
        data_received = self.read_msg()
        self.set_state(self.parse_data(data_received))

    def close_connection(self):
        self.client_socket.close()


if __name__ == "__main__":
    try:
        protocol = Tpp(constants.IP_SERVER)
        protocol.connect_to_server()
        protocol.initialize_game()
        protocol.main_game_loop()
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        protocol.close_connection()
