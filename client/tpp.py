import socket
import constants
import time


class Tpp:
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
        print('***********************************')
        self.client_socket.connect((constants.IP_SERVER, constants.PORT))

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
        data_received = self.read_msg()
        return data_received

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

        # print state
        print('***********************************')
        print('Player 1 paddle: ', self.this_player_paddle)
        print('Player 2 paddle: ', self.other_player_paddle)
        print('Ball x: ', self.ball_x)
        print('Ball y: ', self.ball_y)
        print('Ball speed x: ', self.ball_speed_x)
        print('Ball speed y: ', self.ball_speed_y)
        print('Ball speed: ', self.ball_speed)
        print('***********************************')

    def request_state(self):
        data_received = self.send_msg(constants.GET_STATE)
        if self.parse_data(data_received)[0] == constants.POST_STATE:
            self.set_state(self.parse_data(data_received))

    def register_player(self, nickname):
        data_received = self.send_msg(constants.REGISTER, nickname)
        if self.parse_data(data_received)[0] == constants.SUCC:
            print('Registered successfully!')
        else:
            print('Error registering!')

    def create_room(self):
        data_received = self.send_msg(constants.CREATE)
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
        data_received = self.send_msg(constants.JOIN, game_id)
        parsed_data = self.parse_data(data_received)
        if parsed_data[0] == constants.ERR:
            return data_received[len(constants.ERR) + 1:], True
        elif parsed_data[0] == constants.SUCC:
            return parsed_data[1], False

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

    def main_game_loop(self):
        print(self.player_number)
        data_received = self.read_msg()
        self.set_state(self.parse_data(data_received))

    def close_connection(self):
        self.client_socket.close()


if __name__ == "__main__":
    try:
        protocol = Tpp()
        protocol.connect_to_server()
        protocol.initialize_game()
        protocol.main_game_loop()
        time.sleep(2)
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        protocol.close_connection()
