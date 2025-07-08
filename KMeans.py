import random
import copy
import math


class KMeans:
    def __init__(self, pallete: list[tuple], n_classes: int = 4):
        self.pallete = pallete
        self.n_classters = n_classes
        self.centroids = self.generate_centroids()
        self.classes = [[] for _ in range(self.n_classters)]

    def generate_centroids(self) -> list[tuple]:
        centroids = [
            tuple(random.randint(0, 255) for _ in range(3))
            for _ in range(self.n_classters)
        ]
        return centroids

    def asign_to_centroid(self) -> None:
        for color in self.pallete:
            dist = [
                self._calc_distances(color, self.centroids[i])
                for i in range(self.n_classters)
            ]
            self.classes[dist.index(min(dist))].append(color)

    def recalculate_centroids(self) -> None:
        self.centroids = [
            tuple(sum(col) / len(col) for col in zip(*self.classes[i]))
            for i in range(self.n_classters)
        ]

    def clasterize(self):
        old_centroids = copy.deepcopy(self.centroids)
        self.asign_to_centroid()
        self.recalculate_centroids()
        while old_centroids == self.centroids:
            old_centroids = copy.deepcopy(self.centroids)
            self.asign_to_centroid()
            self.recalculate_centroids()

        print(self.classes)

    @staticmethod
    def _calc_distances(p1: tuple[int, ...], p2: tuple[int, ...]) -> float:
        return math.sqrt(
            (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2
        )


if __name__ == "__main__":
    k_means = KMeans(
        [tuple(random.randint(0, 256) for _ in range(3))
         for _ in range(200)], 4
    )
    k_means.asign_to_centroid()
    k_means.recalculate_centroids()
    k_means.clasterize()
