import networkx as nx
import matplotlib.pyplot as plt

# Inicializa grafo vazia que armazenará nossa rede social
G = nx.Graph()

# Adicionando vértices ao grafo, representando os usuários da rede social
usuarios = ['Pedro', 'Pablo', 'Patrick', 'Letícia', 'Laura', 'Théo', 'Maria']
G.add_nodes_from(usuarios)

# Criando relações de amizade entre os usuários
amizades = [('Pedro', 'Pablo'), ('Pedro', 'Patrick'), ('Pablo', 'Patrick'),
            ('Pablo', 'Letícia'), ('Laura', 'Théo'), ('Théo', 'Maria'), ('Maria', 'Laura')]
G.add_edges_from(amizades)

# Função para encontrar amigo de amigos
def amigos_de_amigos(grafo, usuario):
    amigos = set(grafo.neighbors(usuario))
    amigos_de_amigos_set = set()
    for amigo in amigos:
        amigos_de_amigos_set.update(grafo.neighbors(amigo))
    amigos_de_amigos_set.discard(usuario)
    return amigos_de_amigos_set - amigos

# Encontrando os amigos de amigos de Pedro
pedro = 'Pedro'
fof_pedro = amigos_de_amigos(G, pedro)
print(f'Amigos de amigos de {pedro}: {fof_pedro}')

# Encontra comunidades através de árvores geradoras mínimas
comunidades = list(nx.connected_components(G))
print(f'Comunidades identificadas: {comunidades}')

# Desenha o grafo utilizando nx e plt
posicao = nx.spring_layout(G)
nx.draw(G, posicao, with_labels=True, node_size=500, node_color='lightblue')
plt.show()
