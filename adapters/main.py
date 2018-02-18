import importlib


class Communicator:
    modules = []
    adapters = []

    def __init__(self, adapters):
        for adapter in adapters:
            module = importlib.import_module("adapters." + adapter)
            self.adapters.append(getattr(module, 'Adapter')())
        for adapter in self.adapters:
            adapter.init()

    def process(self, data):
        for adapter in self.adapters:
            adapter.process(data)
