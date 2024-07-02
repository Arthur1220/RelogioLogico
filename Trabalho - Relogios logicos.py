"""
Feito por: Arthur Marques Azevedo
Matricula: 202010234
Disciplina: Sistemas Distribuidos
Descricao do problema:
Programar o algoritmo de relógio de Lamport para sincronização de relógios lógicos com comunicação causal (via relógios vetoriais) utilizando MPI para o caso do exercício anterior. Qualquer linguagem de programação pode ser utilizada.
"""

# Importacao de bibliotecas
from mpi4py import MPI
from time import sleep

# Inicialização do MPI
comm = MPI.COMM_WORLD  # Comunicador MPI que engloba todos os processos
rank = comm.Get_rank()  # Identificador do processo atual
size = comm.Get_size()  # Número total de processos

# Classe que implementa o algoritmo de relógio vetorial
class VectorClock:
    # Inicializa o relógio vetorial para um processo específico.
    def __init__(self, size, rank):
        self.clock = [0] * size
        self.rank = rank

    # Envia uma mensagem para um processo específico.
    def send_message(self, dest):
        self.clock[self.rank] = 1 # Incrementa o relógio local
        comm.send((self.rank, self.clock.copy()), dest=dest) # Envia o relógio atualizado para o processo de destino
        self.print_clock(f"Enviou mensagem para {dest}") # Exibe o relógio atualizado

    # Verifica atrasos na entrega da mensagem, garantindo a condição causal.
    def check_delays(self, received_clock, receive_rank):
        
        # Verificar a condição m[i] = VCj[i] + 1, caso esteja congruente, ira seguir para a proxima verificacao
        if received_clock[receive_rank] != self.clock[receive_rank] + 1:
            print(f"Processo {self.rank} - Atraso detectado da mensagem de {receive_rank} - Primeira condicao")
            return False
        
        # Verificar a condição m[k] <= VCj[k] para todos k diferentes de i
        for i in range(len(self.clock)):
            if i != receive_rank:
                if received_clock[i] > self.clock[i]:
                    print(f"Processo {self.rank} - Atraso detectado da mensagem de {receive_rank} - Segunda condicao")
                    return False

        # Se todas as condicoes forem atendidas, retorna True
        return True
    
    # Recebe uma mensagem de um processo específico.
    def receive_message(self):
        receive_rank, received_clock = comm.recv(source=MPI.ANY_SOURCE) # Recebe o relógio do processo de origem
       
        # Verifica atrasos na entrega da mensagem
        if self.check_delays(received_clock, receive_rank):
            # Atualiza o relógio local com base no relógio recebido
            for i in range(len(self.clock)):
                if received_clock[i] == 1:
                    self.clock[i] = 1
            self.print_clock(f"Recebeu mensagem  de {receive_rank}")

    # Exibe o relógio vetorial do processo.
    def print_clock(self, event):
        print(f"Processo {self.rank} - {event} - Vetor: {self.clock}")

# Função que executa as operações baseadas no arquivo de entrada
def execute_operations(rank, operations):

    # Inicializa o relógio vetorial para o processo atual
    vector_clock = VectorClock(size, rank)

    # Executa cada operação do arquivo de entrada
    for operation in operations:
        sleep(0.1)
        op_parts = operation.split() # Divide a operação em partes
        if int(op_parts[0]) == rank:
            if op_parts[1] == "send_message":
                vector_clock.send_message(int(op_parts[2]))
            elif op_parts[1] == "receive_message":
                vector_clock.receive_message()
            else:
                print(f"Processo {rank} - Operação inválida - {operation}")

    # Retorna o relógio vetorial final do processo
    return vector_clock

# Exibe a quantidade de processos e o vetor inicial de relógios
def initial_print():
    if rank == 0:
        print(f"Quantidade de processos: {size}")
        for i in range(size):
            print(f"Processo {i} - Vetor inicial: {[0] * size}")
        sleep(1)

# Exibe os vetores finais de cada processo
def final_print(process_clocks):
    if rank == 0:
        print("\nFinalizando execução...")
        sleep(1)
        print("\nVetores finais:")
        for i in range(size):
            print(f"Processo {i} - Vetor final: {process_clocks[i].clock}")

# Função principal que coordena a execução do programa
def main():
    initial_print()

    # Leitura do arquivo de entrada
    if rank == 0: # Apenas o processo de rank 0 realiza a leitura do arquivo 
        print("\nLendo o arquivo de entrada... \n")
        sleep(0.5)
        with open('multicast_example.txt', 'r') as file:
        #with open('operations.txt', 'r') as file:
            operations = file.readlines()
        operations = [op.strip() for op in operations]
    else:
        operations = None # Outros processos não realizam a leitura do arquivo

    # Distribuição das operações para todos os processos
    operations = comm.bcast(operations, root=0)

    # Execução das operações
    vector_clock = execute_operations(rank, operations)

    # Coleta dos vetores finais de cada processo
    process_clocks = comm.gather(vector_clock, root=0)

    final_print(process_clocks)

if __name__ == "__main__":
    main()

    # Finalização do MPI
    MPI.Finalize()