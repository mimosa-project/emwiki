from abc import ABCMeta, abstractmethod


class HtmlBuilder(metaclass=ABCMeta):
    from_dir = None
    to_dir = None

    @abstractmethod
    def delete_files(self):
        pass

    @abstractmethod
    def create_files(self, models):
        pass
