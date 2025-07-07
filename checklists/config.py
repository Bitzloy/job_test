from yaml.loader import FullLoader
import os
import yaml


class Config:
    def __init__(self):
        pass

    @classmethod
    def get_abspath(self):
        parent = os.path.abspath(__file__)
        for _ in range(2):
            parent = os.path.dirname(parent)
        return parent

    def get_root_path(self):
        parent = os.path.abspath(__file__)
        for _ in range(1):
            parent = os.path.dirname(parent)
        return parent

    def get_config(self):
        root_path = self.get_root_path()
        with open(root_path + "/config.yaml") as file:
            data = yaml.load(file, Loader=FullLoader)
        return data

    def get_db_path(self):
        db_path = self.get_config()["db_path"]
        return db_path
