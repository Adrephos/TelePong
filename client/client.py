import socket
import struct
import constants

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    print('***********************************')
    print('Client is running...')
    client_socket.connect(("127.0.0.1", constants.PORT))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"quit\" to exit')
    print('Input commands:')
    command_to_send = input()

    while command_to_send != constants.QUIT:
        data_received = ""
        data_received = data_received.encode(constants.ENCONDING_FORMAT)

        client_socket.send(
            bytes(command_to_send, constants.ENCONDING_FORMAT))

        data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)

        print(data_received.decode(constants.ENCONDING_FORMAT))
        command_to_send = input()

    client_socket.send(bytes(command_to_send, constants.ENCONDING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
    print(data_received.decode(constants.ENCONDING_FORMAT))
    print('Closing connection...BYE BYE...')
    client_socket.close()


if __name__ == '__main__':
    main()
