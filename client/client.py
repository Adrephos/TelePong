import socket
import struct
import constants

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    print('***********************************')
    print('Client is running...')
    client_socket.connect((constants.IP_SERVER, constants.PORT))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"quit\" to exit')
    print('Input commands:')
    command_to_send = input()

    def parse_data(data):
        data = data.split(' ')
        return data

    def send_command(command):
        client_socket.send(
            bytes(command, constants.ENCONDING_FORMAT))

        data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)

        return data_received

    while command_to_send != constants.QUIT:
        data_received = ""
        data_received = data_received.encode(constants.ENCONDING_FORMAT)

        method = parse_data(command_to_send)[0]

        if method == constants.QUIT:
            print('Closing connection...BYE BYE...')
            client_socket.close()
            break
        if method == constants.CREATE:
            data_received = send_command(command_to_send)
            print(data_received.decode(constants.ENCONDING_FORMAT))

            data_received = ""
            data_received = data_received.encode(constants.ENCONDING_FORMAT)
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            data_received = data_received.decode(constants.ENCONDING_FORMAT)
            print(data_received)

            if parse_data(data_received)[0] == 'START':
                print('GAME CAN START')
            command_to_send = input()
            continue
        else:
            data_received = send_command(command_to_send)

        if not data_received:
            print('Server closed the connection. Exiting...')
            break  # Exit the loop if the server closed the connection

        print(data_received.decode(constants.ENCONDING_FORMAT))
        command_to_send = input()

    client_socket.send(bytes(command_to_send, constants.ENCONDING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
    print(data_received.decode(constants.ENCONDING_FORMAT))
    print('Closing connection...BYE BYE...')
    client_socket.close()


if __name__ == '__main__':
    main()
