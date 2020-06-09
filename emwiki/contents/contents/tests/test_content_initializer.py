from abc import ABCMeta, abstractmethod


class ContentInitializer(metaclass=ABCMeta):

    def test_initialize(self):
        self._generate_files()
        self._delete_models()
        self._create_models()

    @abstractmethod
    def test_generate_files(self):
        pass

    @abstractmethod
    def test_delete_models(self):
        pass

    @abstractmethod
    def test_create_models(self):
        pass
