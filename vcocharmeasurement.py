class VCOCharMeasurement:

    def __init__(self):
        self.measure_action = lambda: print('vco measure action stub')
        self.params = None
        self.result = None

        self._measure_action_result = None

    def measure(self):
        print(f'vco measure call {self.params}')
        self.measure_action()
        self._measure_action_result = 'VCO CHAR MEASURE ACTION RESULT'
        print(f'result {self._measure_action_result}')

    def process(self):
        print(f'processing {self._measure_action_result}')

        self.result = self._measure_action_result + ' PROCESSED'

        print(f'processed result {self.result}')
