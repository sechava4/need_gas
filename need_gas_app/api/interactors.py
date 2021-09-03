import json
import os
from abc import ABC, abstractmethod

import numpy as np
from sklearn.neighbors import KDTree

from need_gas_app.models import Station

drivers_url = "https://gist.githubusercontent.com" \
                  "/CesarF/41958f4bc34240b75a83fce876836044/" \
                  "raw/b524588cb979fc6e3ec5a8913ee497d64509e888/points.json"

station_repository = "data_sources/stations.json"

current_folder = os.path.dirname(__file__)


class BaseInteractor(ABC):
    @abstractmethod
    def get_nearest(self):
        pass


class DriverInteractor(BaseInteractor):
    def __init__(self, drivers, speed=60, recharge_time=5):
        self.speed_kmh = speed
        self.recharge_time = recharge_time
        self.as_dict = {a.id: a for a in drivers}

        self.kdtree = KDTree(
            np.array([[d.x, d.y] for d in drivers]), leaf_size=2
        )

    def get_nearest(self, client):
        dist, closest = self.kdtree.query([(client.x, client.y)], k=1)
        i = 0
        driver = self.as_dict.get(closest[i][i] + 1)
        return driver, dist[i][i]


class StationInteractor(BaseInteractor):
    def __init__(self, repository=station_repository, model=Station):
        filepath = os.path.join(current_folder, station_repository)
        with open(filepath, "r") as f:
            self.stations = json.loads(f.read())

        self.as_dict = {a.get('id'): Station(**a) for a in self.stations}

        self.kdtree = KDTree(
            np.array([[d['x'], d['y']] for d in self.stations]), leaf_size=2
        )

    def get_nearest(self, client):
        dist, closest = self.kdtree.query([(client.x, client.y)], k=1)
        i = 0
        station = self.as_dict.get(closest[i][i] + 1)
        return station, dist[i][i]
