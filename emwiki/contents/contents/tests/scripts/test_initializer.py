from abc import ABCMeta, abstractmethod


class ContentInitializerTest(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def setUpClass(cls):
        pass

    @classmethod
    @abstractmethod
    def tearDownClass(cls):
        pass

    @abstractmethod
    def test_initialize(self):
        pass

    @abstractmethod
    def test_generate_files(self):
        pass

    @abstractmethod
    def test_delete_models(self):
        pass

    @abstractmethod
    def test_create_models(self):
        pass
