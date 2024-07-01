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
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Algoritmo de relogio vetorial
class VectorClock:
    def __init__(self, size, rank):
        self.clock = [0] * size
        self.rank = rank

    def local_event(self):
        self.clock[self.rank] = 1
        self.print_clock("Evento local")

    def send_message(self, dest):
        self.clock[self.rank] = 1
        comm.send(self.clock.copy(), dest=dest)
        self.print_clock(f"Enviou mensagem para {dest}")

    def check_delays(self, received_clock, sender_rank):
        # Verificar a condição m[i] = VCj[i] + 1
        if received_clock[sender_rank] != self.clock[sender_rank] + 1:
            print(f"Processo {self.rank} - Atraso detectado - Primeira condicao")
            return False
        
        # Verificar a condição m[k] <= VCj[k] para todos k diferentes de i
        for i in range(len(self.clock)):
            if i != sender_rank:
                if received_clock[i] > self.clock[i]:
                    print(f"Processo {self.rank} - Atraso detectado - Segunda condicao")
                    return False

        return True
    
    def receive_message(self):
        received_clock = comm.recv(source=MPI.ANY_SOURCE)
        sender_rank = received_clock.index(max(received_clock))
        if self.check_delays(received_clock, sender_rank):
            for i in range(len(self.clock)):
                if received_clock[i] == 1:
                    self.clock[i] = 1
            self.print_clock("Recebeu mensagem")
            if all(value == 1 for value in self.clock):
                self.print_clock("Recebeu mensagens de todos os processos")

    def print_clock(self, event):
        print(f"Processo {self.rank} - {event} - Vetor: {self.clock}")

# Inicialização do relógio vetorial e execução das operações
def execute_operations(rank, operations):
    vector_clock = VectorClock(size, rank)
    for operation in operations:
        sleep(0.2)
        op_parts = operation.split()
        if op_parts[0] == f'P{rank}':
            if op_parts[1] == "local_event":
                vector_clock.local_event()
            elif op_parts[1] == "send_message":
                vector_clock.send_message(int(op_parts[2]))
            elif op_parts[1] == "receive_message":
                vector_clock.receive_message()
    return vector_clock

# Exibe a quantidade de processos e o vetor inicial de relógios
def initial_print():
    if rank == 0:
        print(f"Quantidade de processos: {size}")
        for i in range(size):
            print(f"Processo {i} - Vetor inicial: {[0] * size}")
        sleep(1)

def final_print(process_clocks):
    if rank == 0:
        print("\nFinalizando execução...")
        sleep(1)
        print("\nVetores finais:")
        for i in range(size):
            print(f"Processo {i} - Vetor final: {process_clocks[i].clock}")
        sleep(0.5)
        print("\nFim da execução")

def main():
    initial_print()

    # Leitura do arquivo de entrada
    if rank == 0:
        print("\nIniciando a leitura do arquivo de operacoes...\n")
        sleep(0.5)
        with open('operations.txt', 'r') as file:
            operations = file.readlines()
        operations = [op.strip() for op in operations]
    else:
        operations = None

    # Distribuição das operações para todos os processos
    operations = comm.bcast(operations, root=0)

    # Execução das operações
    vector_clock = execute_operations(rank, operations)

    # Coleta dos vetores finais de cada processo
    process_clocks = comm.gather(vector_clock, root=0)

    if rank == 0:
        final_print(process_clocks)

if __name__ == "__main__":
    main()

    # Finalização do MPI
    MPI.Finalize()