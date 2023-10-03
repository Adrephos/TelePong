import socket
import constants
import time

class SocketClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_number = 0
        self.this_player_paddle = 0
        self.other_player_paddle = 0
        self.ball_x = 0
        self.ball_y = 0
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.ball_speed = 0

    def connect_to_server(self):
        print('***********************************')
        print('Client is running...')
        print('client_socket:', self.client_socket)
        self.client_socket.connect((constants.IP_SERVER, constants.PORT))
        local_tuple = self.client_socket.getsockname()
        print('Connected to the server from:', local_tuple)
        print('Enter \"quit\" to exit')

    def parse_data(self, data):
        data = data.split(' ')
        return data

    def send_msg(self, msgType, payload=''):
        command = msgType + ' ' + payload
        self.client_socket.send(
            bytes(command, constants.ENCONDING_FORMAT))
        data_received = self.client_socket.recv(constants.RECV_BUFFER_SIZE)
        return data_received.decode(constants.ENCONDING_FORMAT)

    def read_msg(self):
        data_received = ""
        data_received = data_received.encode(constants.ENCONDING_FORMAT)
        data_received = self.client_socket.recv(constants.RECV_BUFFER_SIZE)
        return data_received.decode(constants.ENCONDING_FORMAT)

    def get_state(self):
                # {self.this_player_paddle} ?
        state = f'{self.ball_x} {self.ball_y} ' \
                f'{self.ball_speed_x} {self.ball_speed_y} {self.ball_speed}'
        return state

    def set_state(self, state):
        self.other_player_paddle = int(state[1])
        self.ball_x = int(state[2])
        self.ball_y = int(state[3])
        self.ball_speed_x = int(state[4])
        self.ball_speed_y = int(state[5])
        self.ball_speed = int(state[6])

    def request_state(self):
        data_received = self.send_msg(constants.GET_STATE)
        if self.parse_data(data_received)[0] == constants.POST_STATE:
            self.set_state(self.parse_data(data_received))

    def initialize_game(self):
        # Player registration
        nickname = input('Nickname: ')
        data_received = self.send_msg(constants.REGISTER, nickname)

        # Create or join a room
        create = 'na'
        while create != 'c' and create != 'j':
            create = input('Create or join a room? c/j: ')

        if create == 'c':
            game_id = self.send_msg(constants.CREATE)
            print("Room id: ", game_id.split(' ')[1])
            print('Waiting for another player to join...')
            data_received = self.read_msg()
            if self.parse_data(data_received)[0] == constants.START:
                self.player_number = 1
                print('Game started!')
        elif create == 'j':
            error = True
            while error:
                game_id = input('Room id: ')
                data_received = self.send_msg(constants.JOIN, game_id)
                if data_received.split(' ')[0] == constants.ERR:
                    print(data_received[len(constants.ERR) + 1:])
                else:
                    error = False
                    print('Game started!')
                    self.player_number = 2

    def main_game_loop(self):
        i = 0
        print(self.player_number)
        while True:
            if i != 0:
                self.request_state()
            if self.player_number == 1 and i == 0:
                i += 1
                data_received = self.send_msg(constants.POST_STATE, self.get_state())
            else:
                # Simulate game controls here
                time.sleep(0.2)

    def close_connection(self):
        self.client_socket.close()


if __name__ == "__main__":
    try:
        client = SocketClient()
        client.connect_to_server()
        client.initialize_game()
        client.main_game_loop()
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        client.close_connection()
