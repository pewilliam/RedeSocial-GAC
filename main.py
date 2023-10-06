import random
from faker import Faker

fake = Faker()


# Classe para representar um usuário
class User:
    def __init__(self, name):
        self.name = name
        self.friends = set()  # Conjunto de amigos

    def __lt__(self, other):
        # Comparação personalizada para permitir ordenação de usuários
        return self.name < other.name


# Geração de nomes aleatórios para usuários
def generate_random_names(num_names):
    names = [fake.name() for _ in range(num_names)]
    return names


# Geração de uma rede social simulada com usuários e amizades
def generate_social_network(num_users, max_friends_per_user):
    user_names = generate_random_names(num_users)
    users = [User(name) for name in user_names]

    for user in users:
        num_friends = random.randint(1, max_friends_per_user)
        # Selecionar amigos aleatórios, excluindo o próprio usuário e evitando duplicatas
        friends = random.sample(users, num_friends)
        friends = [friend for friend in friends if friend != user]
        user.friends.update(friends)

    return users


# Função auxiliar para encontrar amigos de segundo grau
def find_second_degree_friends(user, users):
    first_degree_friends = user.friends
    second_degree_friends = set()

    for friend in first_degree_friends:
        second_degree_friends.update(friend.friends)

    # Remover o próprio usuário, amigos de primeiro grau e amigos de segundo grau
    second_degree_friends.discard(user)
    second_degree_friends.difference_update(first_degree_friends)

    return second_degree_friends


# Algoritmo de Kruskal para identificar uma árvore geradora mínima
def kruskal(users):
    edges = []
    for user in users:
        for friend in user.friends:
            if user < friend:  # Correção aqui
                edges.append((user, friend))

    edges.sort()  # Classificar as arestas
    minimum_spanning_tree = set()
    parent = {}  # Para evitar ciclos

    def find(user):
        if user != parent.setdefault(user, user):
            parent[user] = find(parent[user])
        return parent[user]

    for edge in edges:
        user1, user2 = edge
        if find(user1) != find(user2):
            minimum_spanning_tree.add(edge)
            parent[find(user1)] = find(user2)

    return minimum_spanning_tree


# Função para identificar comunidades usando árvores geradoras mínimas
def identify_communities(users, minimum_spanning_tree):
    # Criar um grafo não direcionado com as arestas da árvore geradora mínima
    graph = {}
    for edge in minimum_spanning_tree:
        user1, user2 = edge
        if user1.name not in graph:
            graph[user1.name] = []
        if user2.name not in graph:
            graph[user2.name] = []
        graph[user1.name].append(user2.name)
        graph[user2.name].append(user1.name)

    # Função para encontrar todas as conexões de um usuário
    def dfs(node, visited):
        visited.add(node)
        connections = [node]
        for neighbor in graph[node]:
            if neighbor not in visited:
                connections.extend(dfs(neighbor, visited))
        return connections

    communities = []
    visited_nodes = set()

    for user_name in graph.keys():
        if user_name not in visited_nodes:
            community = dfs(user_name, set())
            communities.append(community)
            visited_nodes.update(community)

    return communities


if __name__ == "__main__":
    num_users = 10
    max_friends_per_user = 3

    users = generate_social_network(num_users, max_friends_per_user)

    # Mostrar usuários e amizades
    print("Nomes de Usuários:")
    for user in users:
        print(user.name)

    print("\nAmizades:")
    for user in users:
        print(f"{user.name} - {[friend.name for friend in user.friends]}")

    # Encontrando amigos de amigos de um usuário aleatório
    user_to_search = random.choice(users)
    friends_of_friends = find_second_degree_friends(user_to_search, users)
    print(f"\nAmigos de amigos de {user_to_search.name}: {[user.name for user in friends_of_friends]}")

    # Identificando árvores geradoras mínimas
    minimum_spanning_tree = kruskal(users)

    # Identificando comunidades
    communities = identify_communities(users, minimum_spanning_tree)

    # Mostra comunidades identificadas
    print("\nComunidades identificadas:")
    for i, community_members in enumerate(communities, start=1):
        print(f"Comunidade {i}: {', '.join(community_members)}")
