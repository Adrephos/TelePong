import socket
import constants

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
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

    # Player registration
    nickname = input('Nickname: ')
    send_msg(constants.REGISTER, nickname)

    # Create or join a room
    create = 'na'
    while create != 'c' and create != 'j':
        create = input('Create or join a room? c/j: ')

    if create == 'c':
        game_id = send_msg(constants.CREATE)
        print("Room id: ", game_id)
        print('Waiting for another player to join...')
        data_received = read_msg()
        if data_received.split(' ')[0] == constants.START:
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

    client_socket.close()


if __name__ == '__main__':
    main()
