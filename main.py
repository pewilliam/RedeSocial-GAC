import random
from faker import Faker

fake = Faker()

class User:
    def __init__(self, name):
        self.name = name
        self.friends = set()

    def __lt__(self, other):
        return self.name < other.name

class Edge:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.distance = 1  # Distância padrão para um grafo não ponderado

def generate_random_names(num_names):
    names = [fake.name() for _ in range(num_names)]
    return names

def generate_social_network(num_users, max_following_per_user):
    user_names = generate_random_names(num_users)
    users = [User(name) for name in user_names]

    for user in users:
        num_following = random.randint(1, max_following_per_user)
        following = random.sample(users, num_following)

        for friend in following:
            if friend != user:
                user.friends.add(friend)

    return users

def kruskal(users):
    edges = []

    # Mapear cada usuário para um valor numérico único
    user_to_id = {user: i for i, user in enumerate(users)}
    id_to_user = {i: user for user, i in user_to_id.items()}

    # Criar uma lista de arestas com base nas conexões de amizade entre os usuários
    for user in users:
        for friend in user.friends:
            if user < friend:  # Evitar duplicatas
                edges.append((user_to_id[user], user_to_id[friend]))

    # Classificar as arestas (não necessária para um grafo não ponderado)
    edges.sort()

    # Implementar o algoritmo de Kruskal para encontrar a árvore de expansão mínima
    mst = []
    parent = {i: i for i in range(len(users))}

    def find(node):
        if parent[node] == node:
            return node
        return find(parent[node])

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            parent[root1] = root2

    for edge in edges:
        user1, user2 = id_to_user[edge[0]], id_to_user[edge[1]]
        if find(edge[0]) != find(edge[1]):
            mst.append((user1, user2))
            union(edge[0], edge[1])

    return mst

def detect_communities_kruskal(users, mst):
    # Usar a árvore de expansão mínima obtida pelo Kruskal para identificar comunidades
    # Neste caso, cada componente conectado na árvore representa uma comunidade
    visited = set()
    communities = []

    def dfs(node, community):
        visited.add(node)
        community.append(node)

        for edge in mst:
            if node == edge[0] and edge[1] not in visited:
                dfs(edge[1], community)
            elif node == edge[1] and edge[0] not in visited:
                dfs(edge[0], community)

    for user in users:
        if user not in visited:
            community = []
            dfs(user, community)
            communities.append(community)

    return communities


def find_friends_of_friends(user):
    friends_of_friends = set()

    for friend in user.friends:
        for friend_of_friend in friend.friends:
            if friend_of_friend != user and friend_of_friend not in user.friends:
                friends_of_friends.add(friend_of_friend)

    return friends_of_friends

if __name__ == "__main__":
    num_users = 6
    max_following_per_user = 2

    users = generate_social_network(num_users, max_following_per_user)

    print("Nomes de Usuários:")
    for user in users:
        print(user.name)

    print("\nRelações:")
    for user in users:
        print(f"{user.name} - {[friend.name for friend in user.friends]}")

    # Use o algoritmo de Kruskal para encontrar a árvore de expansão mínima
    mst = kruskal(users)

    # Use a árvore de expansão mínima para detectar comunidades
    communities = detect_communities_kruskal(users, mst)

    print("\nComunidades identificadas:")
    for i, community in enumerate(communities, start=1):
        print(f"Comunidade {i}: {[user.name for user in community]}")

    print("\nAmigos de Amigos:")
    for user in users:
        friends_of_friends = find_friends_of_friends(user)
        print(f"Amigos de Amigos de {user.name}: {[friend.name for friend in friends_of_friends]}")

