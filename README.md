# Relógio Vetorial com MPI

Este projeto implementa um sistema de sincronização de relógios vetoriais usando MPI (Message Passing Interface) para simular eventos em processos distribuídos. Cada processo executa uma série de eventos, envio e recebimento de mensagens, com os relógios sendo atualizados de acordo.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos e componentes principais:

### Arquivos

1. **`vector_clock.py`**:
   - Este é o arquivo principal do projeto que contém a implementação do algoritmo de relógio vetorial usando MPI.
   - Inclui a definição da classe `VectorClock`, que gerencia o vetor de relógios para cada processo.
   - Implementa as operações de evento local (`local_event`), envio de mensagem (`send_message`) e recebimento de mensagem (`receive_message`).
   - Contém funções auxiliares para a impressão do estado dos relógios e para a verificação de atrasos na entrega das mensagens (`check_delays`).
   - Define a função `execute_operations`, que executa uma sequência de operações definidas no arquivo de entrada.
   - Inclui a lógica para a inicialização do MPI, a distribuição das operações entre os processos, e a coleta e impressão dos vetores finais dos relógios.

2. **`operations.txt`**:
   - Arquivo de entrada que especifica a sequência de operações que cada processo deve realizar.
   - Cada linha do arquivo representa uma operação que um processo específico deve executar.
   - As operações possíveis são: `local_event`, `send_message <dest>`, e `receive_message`.

### Classes e Funções

1. **Classe `VectorClock`**:
   - **`__init__(self, size, rank)`**: Inicializa o vetor de relógios com zeros e define o rank do processo.
   - **`local_event(self)`**: Incrementa o contador do processo local e imprime o estado atual do vetor de relógios.
   - **`send_message(self, dest)`**: Incrementa o contador do processo local, envia o vetor de relógios para o processo de destino, e imprime o estado atual do vetor de relógios.
   - **`receive_message(self)`**: Recebe um vetor de relógios de qualquer processo, verifica atrasos usando `check_delays`, e atualiza o vetor de relógios local.
   - **`check_delays(self, received_clock, sender_rank)`**: Verifica atrasos na entrega de mensagens baseado nas condições de causalidade.
   - **`print_clock(self, event)`**: Imprime o estado atual do vetor de relógios com uma descrição do evento ocorrido.

2. **Funções Auxiliares**:
   - **`execute_operations(rank, operations)`**: Executa as operações especificadas para um dado processo. As operações são lidas do arquivo de entrada e distribuídas para cada processo.
   - **`initial_print()`**: Imprime a quantidade de processos e os vetores de relógios iniciais para cada processo.
   - **`final_print(process_clocks)`**: Coleta e imprime os vetores finais de relógios para todos os processos no final da execução.
   - **`main()`**: Função principal que inicializa o MPI, lê e distribui as operações, executa as operações para cada processo, e imprime os vetores de relógios finais.

### Funcionamento do Algoritmo

1. **Inicialização**:
   - O MPI é inicializado e os processos obtêm seus ranks e o tamanho total da comunicação.
   - Cada processo inicializa seu vetor de relógios com zeros.

2. **Leitura e Distribuição de Operações**:
   - O processo com rank 0 lê o arquivo `operations.txt` e distribui as operações para todos os processos usando `comm.bcast`.

3. **Execução das Operações**:
   - Cada processo executa suas operações conforme especificado no arquivo de entrada.
   - Para `local_event`, o contador do processo local é incrementado.
   - Para `send_message`, o contador do processo local é incrementado e o vetor de relógios é enviado ao processo de destino.
   - Para `receive_message`, o vetor de relógios é recebido de outro processo, verificado para atrasos, e o vetor local é atualizado conforme necessário.

4. **Verificação de Atrasos**:
   - A função `check_delays` garante que a entrega de mensagens respeite a causalidade, verificando se o vetor de relógios recebido satisfaz as condições de causalidade.

5. **Finalização**:
   - Após a execução de todas as operações, os vetores de relógios finais são coletados e impressos.

Esta estrutura detalhada oferece uma visão abrangente do funcionamento do algoritmo de relógio vetorial e da interação entre os componentes do projeto.

## Como Executar

1. **Pré-requisitos**: Certifique-se de ter `mpi4py` instalado:
   ```bash
   pip install mpi4py
   ```

2. **Arquivo de Entrada**: Crie um arquivo `operations.txt` com a sequência de operações. O formato do arquivo deve ser:

   ```
   P0 send_message 1
   P0 send_message 3
   P1 receive_message
   P1 send_message 2
   P1 send_message 3
   P2 receive_message
   P2 send_message 3
   P3 receive_message
   P3 receive_message
   P3 receive_message
   ```

   Cada linha representa uma operação que um processo deve realizar. As operações são:

   - `local_event`: Evento local no processo.
   - `send_message <dest>`: Envia uma mensagem para o processo de destino.
   - `receive_message`: Recebe uma mensagem de qualquer processo.

   **Possibilidades de Entrada para 4 Processos**

   Aqui estão todas as possíveis entradas com 4 processos, incluindo as operações de envio e recebimento de mensagens entre os processos:

   ```txt
   P0 send_message 1
   P0 send_message 2
   P0 send_message 3
   P1 receive_message
   P2 receive_message
   P3 receive_message
   P1 send_message 0
   P1 send_message 2
   P1 send_message 3
   P0 receive_message
   P2 receive_message
   P3 receive_message
   P2 send_message 0
   P2 send_message 1
   P2 send_message 3
   P0 receive_message
   P1 receive_message
   P3 receive_message
   P3 send_message 0
   P3 send_message 1
   P3 send_message 2
   P0 receive_message
   P1 receive_message
   P2 receive_message
   ```

3. **Execução do Programa**: Para rodar o programa com MPI, execute o seguinte comando:

   ```bash
   mpirun -np 4 python 'Trabalho - Relogios logicos.py'
   ```

   Onde `-np 4` especifica o número de processos MPI.

## Saída do Programa

O programa imprimirá o estado atual do vetor de relógios junto com o evento que ocorreu para cada processo. Exemplo de saída:

```
Quantidade de processos: 4
Processo 0 - Vetor inicial: [0, 0, 0, 0]
Processo 1 - Vetor inicial: [0, 0, 0, 0]
Processo 2 - Vetor inicial: [0, 0, 0, 0]
Processo 3 - Vetor inicial: [0, 0, 0, 0]

Processo 0 - Evento local - Vetor: [1, 0, 0, 0]
Processo 0 - Enviou mensagem para 1 - Vetor: [1, 0, 0, 0]
Processo 1 - Recebeu mensagem - Vetor: [1, 1, 0, 0]
Processo 1 - Enviou mensagem para 0 - Vetor: [1, 1, 0, 0]
Processo 0 - Recebeu mensagem - Vetor: [1, 1, 0, 0]

Finalizando execução...

Vetores finais:
Processo 0 - Vetor final: [1, 1, 0, 0]
Processo 1 - Vetor final: [1, 1, 0, 0]
Processo 2 - Vetor final: [0, 0, 0, 0]
Processo 3 - Vetor final: [0, 0, 0, 0]

Fim da execução
```

## Explicação do Relógio Vetorial

O relógio vetorial é uma estrutura de dados usada para capturar a causalidade entre eventos em sistemas distribuídos. Cada processo mantém um vetor de contadores, onde cada contador corresponde a um processo no sistema.

### Operações

- **Evento Local**: Incrementa o contador do processo local.
- **Enviar Mensagem**: Incrementa o contador do processo local e envia o vetor de relógios atual para o processo de destino.
- **Receber Mensagem**: Recebe o vetor de relógios de outro processo e atualiza o vetor local para refletir a causalidade.

Ao receber uma mensagem, o processo atualiza seu vetor de relógios tomando o máximo valor de cada posição entre seu próprio vetor e o vetor recebido. Isso garante que o vetor de relógios capture a causalidade completa dos eventos.