class VCOCharMeasurement:

    def __init__(self):
        self.measure = None
        self.params = None
        self.result = None

    def process(self):
        print(f'processing {self.params}')

        print(f'processed result {self.result}')
