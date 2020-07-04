class ContentInitializer:
    def __init__(self, builder):
        self.builder = builder

    def initialize(self):
        self.builder.delete_models()
        self.builder.create_models()
