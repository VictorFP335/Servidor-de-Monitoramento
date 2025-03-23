# Servidor de Monitoramento de Recursos

Este projeto foi desenvolvido como parte do curso de **Ciência de Dados** na **PUC-Campinas**. O objetivo é criar um servidor que monitora o uso de CPU e Memória de um sistema, permitindo que clientes se conectem e recebam essas informações em tempo real.

##  Funcionalidades
- Monitoramento de CPU e Memória.
- Limite de 3 clientes conectados simultaneamente.
- Desconexão automática após 1 minuto e meio de inatividade.
- Tratamento de erros e opções inválidas.

##  Como executar

### Servidor
1. Certifique-se de ter o Python instalado.
2. Instale as dependências necessárias:
   ```bash
   pip install psutil
   ```
3. Execute o servidor:
   ```bash
   python servidor.py
   ```

### Cliente
1. Execute o cliente:
   ```bash
   python cliente.py
   ```
2. Escolha uma das opções disponíveis no menu interativo.

##  Controles do Cliente
1. Monitorar CPU
2. Monitorar Memória
3. Parar Monitoramento
4. Mostrar Timer
5. Desconectar

##  Requisitos
- Python 3.x
- Biblioteca `psutil`

##  Desenvolvido por
- **Veronica** - RA: 21943055
- **Victor** - RA: 23007606

