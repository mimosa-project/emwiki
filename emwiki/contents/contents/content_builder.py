from abc import ABCMeta, abstractmethod


class ContentBuilder(metaclass=ABCMeta):
    from_dir = None

    def __init__(self):
        self.objects = []

    @abstractmethod
    def delete_models(self):
        pass

    @abstractmethod
    def create_models(self):
        pass
