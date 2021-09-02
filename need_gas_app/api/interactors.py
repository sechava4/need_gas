from sklearn.neighbors import KDTree
import numpy as np


class DriverInteractor:
    drivers_url = "https://gist.githubusercontent.com" \
                  "/CesarF/41958f4bc34240b75a83fce876836044/" \
                  "raw/b524588cb979fc6e3ec5a8913ee497d64509e888/points.json"
    speed_kmh = 60

    def __init__(self, drivers):
        self.as_dict = {a.id: a for a in drivers}

        self.kdtree = KDTree(
            np.array([[d.x, d.y] for d in drivers]), leaf_size=2
        )

    def get_nearest(self, client, i):
        dist, closest = self.kdtree.query([(client.x, client.y)], k=1)
        i -= 1
        driver = self.as_dict.get(closest[i][i])
        driver["distance"] = dist[i][i]
        driver["minutes"] = 60 * driver["distance"] / self.speed_kmh
        return driver
