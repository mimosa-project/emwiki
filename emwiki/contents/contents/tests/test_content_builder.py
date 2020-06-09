from abc import ABCMeta, abstractmethod


class ContentBuilder(metaclass=ABCMeta):
    @abstractmethod
    def test_bulk_build(self, from_dir, to_dir):
        pass
