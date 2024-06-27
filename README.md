# Relógio Vetorial com MPI

Este projeto implementa um sistema de sincronização de relógios vetoriais usando MPI (Message Passing Interface) para simular eventos em processos distribuídos. Cada processo executa uma série de eventos, incluindo eventos locais, envio e recebimento de mensagens, com os relógios sendo atualizados de acordo.

## Estrutura do Projeto

- `vector_clock.py`: Código principal que executa a simulação.
- `operations.txt`: Arquivo de entrada contendo a sequência de operações que cada processo deve realizar.

## Como Executar

1. **Pré-requisitos**: Certifique-se de ter `mpi4py` instalado:
   ```bash
   pip install mpi4py
   ```

2. **Arquivo de Entrada**: Crie um arquivo `operations.txt` com a sequência de operações. O formato do arquivo deve ser:

   ```
   P0 local_event
   P0 send_message 1
   P0 receive_message
   P0 local_event
   P1 receive_message
   P1 send_message 0
   P1 local_event
   P1 receive_message
   ```

   Cada linha representa uma operação que um processo deve realizar. As operações são:

   - `local_event`: Evento local no processo.
   - `send_message <dest>`: Envia uma mensagem para o processo de destino.
   - `receive_message`: Recebe uma mensagem de qualquer processo.

3. **Execução do Programa**: Para rodar o programa com MPI, execute o seguinte comando:

   ```bash
   mpirun -np 4 python vector_clock.py
   ```

   Onde `-np 4` especifica o número de processos MPI.

## Saída do Programa

O programa imprimirá o estado atual do vetor de relógios junto com o evento que ocorreu para cada processo. Exemplo de saída:

```
Processo 0 - Evento local - Vetor: [1, 0, 0, 0]
Processo 0 - Enviou mensagem para 1 - Vetor: [1, 0, 0, 0]
Processo 0 - Recebeu mensagem - Vetor: [1, 1, 0, 0]
Processo 0 - Evento local - Vetor: [2, 1, 0, 0]
Processo 1 - Recebeu mensagem - Vetor: [1, 1, 0, 0]
Processo 1 - Enviou mensagem para 0 - Vetor: [1, 1, 0, 0]
Processo 1 - Evento local - Vetor: [1, 2, 0, 0]
Processo 1 - Recebeu mensagem - Vetor: [1, 2, 0, 0]
```

## Explicação do Relógio Vetorial

O relógio vetorial é uma estrutura de dados usada para capturar a causalidade entre eventos em sistemas distribuídos. Cada processo mantém um vetor de contadores, onde cada contador corresponde a um processo no sistema.

### Operações

- **Evento Local**: Incrementa o contador do processo local.
- **Enviar Mensagem**: Incrementa o contador do processo local e envia o vetor de relógios atual para o processo de destino.
- **Receber Mensagem**: Recebe o vetor de relógios de outro processo e atualiza o vetor local para refletir a causalidade.

Ao receber uma mensagem, o processo atualiza seu vetor de relógios tomando o máximo valor de cada posição entre seu próprio vetor e o vetor recebido. Isso garante que o vetor de relógios capture a causalidade completa dos eventos.

## Possibilidades de Entrada para 4 Processos

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

### Exemplo de Arquivo `operations.txt`

```txt
P0 local_event
P0 send_message 1
P1 receive_message
P1 send_message 2
P2 receive_message
P2 send_message 3
P3 receive_message
P3 send_message 0
P0 receive_message
P0 local_event
P1 local_event
P2 local_event
P3 local_event
```

### Executando o Programa

Para executar o programa com o arquivo de operações acima, salve o conteúdo em `operations.txt` e execute:

```bash
mpirun -np 4 python vector_clock.py
```

## Contribuição

Sinta-se à vontade para contribuir com melhorias para este projeto. Qualquer sugestão ou correção é bem-vinda.