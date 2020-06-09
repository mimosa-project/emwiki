from abc import ABCMeta, abstractmethod


class ContentSearcher(metaclass=ABCMeta):

    @abstractmethod
    def test_search(self, query_text):
        pass
