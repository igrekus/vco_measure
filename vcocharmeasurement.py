class VCOCharMeasuredResult:

    def __init__(self, volt, freq, kvco, current, power, pushing, noise):
        self.volt = volt
        self.freq = freq
        self.kvco = kvco
        self.current = current
        self.power = power
        self.pushing = pushing
        self.noise = noise


class VCOCharProcessedResult:

    def __init__(self, raw_result):
        self.raw = raw_result

        self._process()

    def _process(self):
        print('process')

    @property
    def tune_voltage(self):
        return self.raw.volt
    @property
    def frequency(self):
        return self.raw.freq
    @property
    def kvco(self):
        return self.raw.kvco
    @property
    def supply_current(self):
        return self.raw.current
    @property
    def power(self):
        return self.raw.power
    @property
    def pushing(self):
        return self.raw.pushing
    @property
    def noise(self):
        return self.raw.noise


class VCOCharMeasurement:

    def __init__(self):
        self.measure_action = lambda: ([0], [0])
        self.params = None

        self._measure_action_result = None
        self.result = None

    def measure(self):
        print(f'vco measure call {self.params}')

        volt, freq = self.measure_action()
        self._measure_action_result = VCOCharMeasuredResult(volt, freq, freq, freq, freq, freq, freq)

        print(f'result {self._measure_action_result}')

    def process(self):
        print(f'processing {self._measure_action_result}')

        self.result = VCOCharProcessedResult(self._measure_action_result)

        print(f'processed result {self.result}')
