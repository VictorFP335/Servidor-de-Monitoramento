'''
                                        TRABALHO DE REDES DE COMPUTADORES


                                                  INTEGRANTES 

 NOME: Veronica
 RA: 21943055

NOME: Victor
RA: 23007606

                                             CÓDIGO                                                   
'''

# BIBLIOTECA USADA
import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

def receber_dados(cliente_socket):
    while True:
        try:
            resposta = cliente_socket.recv(1024).decode().strip()
            if not resposta:
                break
            print(resposta)
        except:
            break

def iniciar_cliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente_socket.connect((SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return

    thread_receber = threading.Thread(target=receber_dados, args=(cliente_socket,))
    thread_receber.daemon = True
    thread_receber.start()

    while True:
        comando = input().strip()

        if comando in ["1", "2", "3", "4", "5"]:
            cliente_socket.send(comando.encode())
            if comando == "5":
                break
        else:
            print("Opção inválida! Digite um número entre 1 e 5.")

    cliente_socket.close()
    print("Desconectado do servidor.")

if __name__ == "__main__":
    iniciar_cliente()
