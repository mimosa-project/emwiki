from abc import ABCMeta, abstractmethod


class ContentInitializer(metaclass=ABCMeta):

    def initialize(self):
        self._generate_files()
        self._delete_models()
        self._create_models()

    @abstractmethod
    def _generate_files(self):
        pass

    @abstractmethod
    def _delete_models(self):
        pass

    @abstractmethod
    def _create_models(self):
        pass
