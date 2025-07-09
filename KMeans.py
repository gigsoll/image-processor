import random
import math


class KMeans:
    def __init__(self, pallete: list[tuple], common_colors: list[tuple]):
        self.pallete = pallete
        self.n_classters = len(common_colors)
        self.centroids = common_colors
        self.classes = [[] for _ in range(self.n_classters)]

    def asign_to_centroid(self) -> dict[tuple, list]:
        """
        Asigns points in data (colors) to centroids based on distance
        """
        for color in self.pallete:
            dist = [
                self._calc_distances(color, self.centroids[i])
                for i in range(self.n_classters)
            ]
            self.classes[dist.index(min(dist))].append(color)
        return dict(zip(self.pallete, self.classes))

    @staticmethod
    def _calc_distances(p1: tuple[int, ...], p2: tuple[int, ...]) -> float:
        return math.sqrt(
            (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2
        )


if __name__ == "__main__":
    k_means = KMeans(
        [tuple(random.randint(0, 255) for _ in range(3)) for _ in range(120)], 10
    )
    k_means.clasterize()
    k_means.classes
