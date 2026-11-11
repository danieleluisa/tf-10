from collections import deque

class MiniGit:
    __slots__ = (
        '_dicionario_pais', 
        '_dicionario_mensagens', 
        '_dicionario_branches', 
        '_branch_atual', 
        '_contador_id', 
        '_passos_ultima_operacao'
    )

    def __init__(self):
        self._dicionario_pais = {}
        self._dicionario_mensagens = {}
        self._dicionario_branches = {"main": None}
        self._branch_atual = "main"
        self._contador_id = 0
        self._passos_ultima_operacao = 0

    @property
    def passos(self):
        return self._passos_ultima_operacao

    @property
    def branch_atual(self):
        return self._branch_atual

    def _gerar_id(self):
        self._contador_id += 1
        return f"c{self._contador_id}"

    def commitar(self, mensagem):
        if not mensagem:
            raise ValueError("A mensagem do commit nao pode ser vazia.")
        
        novo_id = self._gerar_id()
        pai_atual = self._dicionario_branches[self._branch_atual]

        if pai_atual is None:
            self._dicionario_pais[novo_id] = []
        else:
            self._dicionario_pais[novo_id] = [pai_atual]

        self._dicionario_mensagens[novo_id] = mensagem
        self._dicionario_branches[self._branch_atual] = novo_id
        
        self._passos_ultima_operacao = 2
        return novo_id

    def mensagem(self, commit):
        if commit not in self._dicionario_mensagens:
            raise ValueError(f"O commit {commit} nao existe.")
        
        self._passos_ultima_operacao = 1
        return self._dicionario_mensagens[commit]

    def pais(self, commit):
        if commit not in self._dicionario_pais:
            raise ValueError(f"O commit {commit} nao existe.")
        
        self._passos_ultima_operacao = 1
        return tuple(self._dicionario_pais[commit])

    def criar_branch(self, nome):
        if nome in self._dicionario_branches:
            raise ValueError(f"A branch {nome} ja existe.")
        
        commit_atual = self._dicionario_branches[self._branch_atual]
        if commit_atual is None:
            raise ValueError("Nao ha commits para criar uma branch.")
        
        self._dicionario_branches[nome] = commit_atual
        self._passos_ultima_operacao = 1

    def trocar_branch(self, nome):
        if nome not in self._dicionario_branches:
            raise ValueError(f"A branch {nome} nao existe.")
        
        self._branch_atual = nome
        self._passos_ultima_operacao = 1

    def mesclar(self, nome):
        if nome not in self._dicionario_branches:
            raise ValueError(f"A branch {nome} nao existe.")
        if nome == self._branch_atual:
            raise ValueError("Nao e possivel mesclar a branch com ela mesma.")

        commit_alvo = self._dicionario_branches[nome]
        commit_atual = self._dicionario_branches[self._branch_atual]

        if commit_alvo is None or commit_atual is None:
            raise ValueError("Branch vazia nao pode ser mesclada.")

        novo_id = self._gerar_id()
        self._dicionario_pais[novo_id] = [commit_atual, commit_alvo]
        self._dicionario_mensagens[novo_id] = f"merge de {nome}"
        self._dicionario_branches[self._branch_atual] = novo_id
        
        self._passos_ultima_operacao = 2
        return novo_id

    def log(self):
        commit_inicial = self._dicionario_branches[self._branch_atual]
        if commit_inicial is None:
            return ()

        fila = deque([commit_inicial])
        visitados = set()
        resultado = []
        passos_contados = 0

        while fila:
            atual = fila.popleft()
            passos_contados += 1  
            
            if atual not in visitados:
                visitados.add(atual)
                resultado.append(atual)
                for pai in self._dicionario_pais.get(atual, []):
                    fila.append(pai)

        self._passos_ultima_operacao = passos_contados
        return tuple(resultado)

    def buscar(self, texto):
        passos_contados = 0
        encontrado = None

        for commit_id, mensagem_texto in self._dicionario_mensagens.items():
            passos_contados += 1
            if texto in mensagem_texto:
                encontrado = commit_id
                break

        self._passos_ultima_operacao = passos_contados
        return encontrado

    def merges(self):
        passos_contados = 0
        resultado = []

        for commit_id, lista_pais in self._dicionario_pais.items():
            passos_contados += 1
            if len(lista_pais) > 1:
                resultado.append(commit_id)

        self._passos_ultima_operacao = passos_contados
        return tuple(resultado)


def tentar(acao):
    try:
        acao()
    except ValueError as erro:
        print(f"erro: {erro}")


def testar():
    git = MiniGit()
    git.commitar("primeiro commit")
    print(git.passos)
    
    git.commitar("segundo commit")
    git.criar_branch("feature")
    print(git.passos)
    
    git.commitar("terceiro commit")
    git.trocar_branch("feature")
    git.commitar("quarto commit")
    git.trocar_branch("main")
    git.mesclar("feature")
    
    print(git.pais("c5"))
    print(git.log(), git.passos)
    print(git.mensagem("c3"), git.passos)
    print(git.buscar("quarto"), git.passos)
    print(git.merges())
    
    git.trocar_branch("feature")
    print(git.log(), git.passos)
    git.trocar_branch("main")

    print("\n--- Testando Erros Esperados ---")
    tentar(lambda: git.trocar_branch("inexistente"))
    tentar(lambda: git.criar_branch("main"))
    tentar(lambda: git.mesclar("main"))
    tentar(lambda: git.pais("c99"))


def medir(quantidade):
    git = MiniGit()
    for i in range(quantidade):
        git.commitar(f"commit {i}")
    
    passos_commit = git.passos
    git.log()
    passos_log = git.passos
    return passos_commit, passos_log


if __name__ == "__main__":
    testar()
    print("\n--- Tabela de Medição (Leitura x Escrita) ---")
    print("commits  passos do commitar  passos do log")
    for q in [10, 100, 1000]:
        pc, pl = medir(q)
        print(f"{q:<8} {pc:<19} {pl}")