from abc import ABCMeta, abstractmethod


class ContentSearcher(metaclass=ABCMeta):

    @abstractmethod
    def search(self, query_text):
        pass
