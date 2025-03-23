'''
                                        TRABALHO DE REDES DE COMPUTADORES


                                                  INTEGRANTES 


                                                    DESCRIÇÃO 
        
        VERSÃO USADA PARA EXECUÇÃO DO CÓDIGO PYTHON 3.11

 NOME: Veronica
 RA: 21943055

NOME: Victor
RA: 23007606

                                             CÓDIGO                                                   
'''
# BIBLIOTECA USADA
import socket
import threading
import psutil
import time
from datetime import datetime

# Configurações do servidor
HOST = "127.0.0.1"
PORT = 5000
MAX_CLIENTES = 3  # Máximo de clientes simultâneos
TEMPO_INATIVIDADE = 30  # Tempo antes da desconexão por inatividade (segundos)

clientes = {}  # Dicionário para armazenar clientes e tempos de atividade
lock = threading.Lock()

def handle_cliente(cliente_socket, endereco):
    global clientes
    print(f"[NOVA CONEXÃO] Cliente {endereco} conectado.")

    with lock:
        if len(clientes) >= MAX_CLIENTES:
            cliente_socket.send("Número máximo de usuários atingido. Tente mais tarde.\n".encode())
            cliente_socket.close()
            return
        clientes[cliente_socket] = time.time()

    cliente_socket.send(f"{datetime.now().strftime('%H:%M:%S')}: CONECTADO!!\n".encode())

    monitorando = None
    while True:
        try:#Funcionalidades
            cliente_socket.send("\nEscolha uma opção:\n"
                                "1 - Monitorar CPU\n"
                                "2 - Monitorar Memória\n"
                                "3 - Parar Monitoramento\n"
                                "4 - Mostrar Timer\n"
                                "5 - Desconectar\n"
                                "Digite a opção: ".encode())

            cliente_socket.settimeout(TEMPO_INATIVIDADE)
            msg = cliente_socket.recv(1024).decode().strip()
            clientes[cliente_socket] = time.time()  # Atualiza tempo de atividade

            if not msg:
                break
#Ifs de cada opção para usuario
            if msg == "1":
                monitorando = "cpu"
                cliente_socket.send("Monitorando CPU...\n".encode())
            elif msg == "2":
                monitorando = "memoria"
                cliente_socket.send("Monitorando Memória...\n".encode())
            elif msg == "3":
                monitorando = None
                cliente_socket.send("Monitoramento Parado.\n".encode())
            elif msg == "4":
                cliente_socket.send(f"Timer: {datetime.now().strftime('%H:%M:%S')}\n".encode())
            elif msg == "5":
                break
            else:
                cliente_socket.send("Opção inválida! Escolha entre 1 a 5.\n".encode())
                continue  # Volta para pedir nova entrada sem iniciar o loop de monitoramento

            while monitorando:
                if monitorando == "cpu":
                    uso_cpu = psutil.cpu_percent(interval=1)
                    cliente_socket.send(f"Uso de CPU: {uso_cpu}%\n".encode())
                elif monitorando == "memoria":
                    uso_memoria = psutil.virtual_memory().percent
                    cliente_socket.send(f"Uso de Memória: {uso_memoria}%\n".encode())

                clientes[cliente_socket] = time.time()

                # Verifica se há um novo comando do cliente antes do próximo envio
                cliente_socket.settimeout(5)  # Timeout curto para receber novos comandos
                try:
                    novo_msg = cliente_socket.recv(1024).decode().strip()
                    if novo_msg in ["1", "2", "3", "4", "5"]:
                        msg = novo_msg  # Atualiza para processar a nova opção
                        break  # Sai do loop de monitoramento para processar a nova escolha
                except socket.timeout:
                    pass  # Continua monitorando se não houver nova entrada do usuário
#Bloqueio por inatividade
        except socket.timeout:
            print(f"[INATIVIDADE] Cliente {endereco} desconectado por inatividade.")
            break

        except Exception as e:
            print(f"Erro: {e}")
            break

    with lock:
        if cliente_socket in clientes:
            del clientes[cliente_socket]
    cliente_socket.close()
    print(f"[DESCONECTADO] Cliente {endereco} saiu.")
#Iniciação de serviodr
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(MAX_CLIENTES)
    print(f"[SERVIDOR] Rodando em {HOST}:{PORT}")

    while True:
        cliente_socket, endereco = servidor.accept()
        thread = threading.Thread(target=handle_cliente, args=(cliente_socket, endereco))
        thread.start()
#script executado
if __name__ == "__main__":
    iniciar_servidor()
