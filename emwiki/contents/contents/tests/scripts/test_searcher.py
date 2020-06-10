from abc import ABCMeta, abstractmethod


class ContentSearcherTest(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def setUpClass(cls):
        pass

    @classmethod
    @abstractmethod
    def tearDownClass(cls):
        pass

    @abstractmethod
    def test_search(self):
        pass
