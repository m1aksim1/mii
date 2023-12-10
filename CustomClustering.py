import numpy as np


class DBSCAN:
    def __init__(self, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = None

    def fit(self, X):
        n = X.shape[0]
        visited = np.full(n, False)
        self.labels = np.zeros(n, dtype=int)
        cluster_id = 0

        for i in range(n):
            print(i)
            if not visited[i]:
                visited[i] = True
                neighbors = self._get_neighbors(X, i)
                if len(neighbors) < self.min_samples:
                    self.labels[i] = -1
                else:
                    cluster_id += 1
                    self._expand_cluster(X, i, neighbors, visited, cluster_id)
        return self.labels

    def _expand_cluster(self, X, point_index, neighbors, visited, cluster_id):
        self.labels[point_index] = cluster_id
        i = 0
        while i < len(neighbors):
            neighbor_index = neighbors[i]
            if not visited[neighbor_index]:
                visited[neighbor_index] = True
                new_neighbors = self._get_neighbors(X, neighbor_index)
                if len(new_neighbors) >= self.min_samples:
                    neighbors = np.append(neighbors, new_neighbors)
            if self.labels[neighbor_index] == 0:
                self.labels[neighbor_index] = cluster_id
            i += 1

    def _get_neighbors(self, X, point_index):
        distances = np.linalg.norm(X - X[point_index], axis=1)
        return np.where(distances < self.eps)[0]