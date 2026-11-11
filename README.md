# TF 10: MiniGit

## Tabela de Medição

| commits | passos do commitar | passos do log |
| :--- | :--- | :--- |
| 10 | 2 | 10 |
| 100 | 2 | 100 |
| 1000 | 2 | 1000 |

## Respostas

1. **Por que o commitar gasta sempre 2 passos, e o log gasta mais conforme o histórico cresce? (Leitura x Escrita)**  
O commit realiza operações diretas e pontuais de inserção no dicionário (um passo para criar o nó e outro para atualizar o ponteiro da branch), mantendo o custo O(1) constante. Já o método log precisa percorrer todo o histórico de nós alcançáveis utilizando busca em largura (BFS), visitando cada commit do grafo, o que faz o custo crescer de forma linear O(N) proporcionalmente ao tamanho do histórico.

2. **Por que mensagem(commit) gasta 1 passo e buscar(texto) pode gastar muitos? O que o dicionário ganha quando se procura pela chave, e o que ele não ajuda quando se procura pelo valor?**  
O método mensagem acessa diretamente a chave do dicionário de mensagens, operação instantânea de acesso em tempo constante O(1). Em contrapartida, o método buscar precisa iterar por todos os valores armazenados para comparar strings textuais, pois dicionários em Python são otimizados para busca rápida por chave, mas não indexam os valores internamente, exigindo uma varredura sequencial.

3. **Por que o merge é um commit com dois pais, e por que isso faz do histórico um grafo, e não uma lista?**  
O merge une duas linhas de desenvolvimento divergentes, recolhendo os estados correntes da branch atual e da branch alvo como origens simultâneas. Como um commit passa a ter múltiplos antecessores, a estrutura deixa de ser linear (lista) e passa a se comportar como um grafo direcionado acíclico (DAG).

4. **Por que o método pais devolve uma tupla, e não a lista que está guardada dentro do dicionário?**  
Devolver uma tupla protege o encapsulamento e a integridade interna do histórico, impedindo que partes externas do código modifiquem ou corrompam acidentalmente as listas de referência dos pais armazenadas nos dicionários privados da classe.