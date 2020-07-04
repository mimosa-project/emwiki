class HtmlInitializer:
    def __init__(self, builder):
        self.builder = builder

    def initialize(self, models):
        self.builder.delete_files()
        self.builder.create_files(models)
