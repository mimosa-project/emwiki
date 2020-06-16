from abc import ABCMeta, abstractmethod


class ContentBuilder(metaclass=ABCMeta):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

