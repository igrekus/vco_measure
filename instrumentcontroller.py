import time

from instr.pna20 import Pna20

is_mock = True


def parse_measure_string(string: str):
    return [float(point) for point in string.split(',')]


class InstrumentController:

    def __init__(self, ip='169.254.9.227'):
        self._ip = ip
        self._analyzer: Pna20 = None

    def _find_analyzer(self):
        if is_mock:
            from instr.pna20mock import Pna20Mock
            self._analyzer = Pna20Mock(Pna20Mock.idn)
            return

        from instr.pna20 import Pna20

        if self._ip:
            print(f'trying {self._ip}')
            try:
                self._analyzer = Pna20.from_address_string(self.analyzer_address)
                return
            except Exception as ex:
                print('analyzer find error:', ex)

        if not self._analyzer:
            print('analyzer not found, giving up')

    def find(self):
        print('find analyzer')
        try:
            self._find_analyzer()
        except Exception as ex:
            print(ex)
        print(f'analyzer: {self._analyzer}')

        return bool(self._analyzer)

    def test_sample(self):
        return True

    def measure(self, params):
        print(params)

        self._analyzer.reset()
        self._analyzer.source_supply_voltage(supply=1, volt=4.7)
        self._analyzer.source_supply_status(supply=1, status='ON')
        self._analyzer.source_supply_voltage(supply=2, volt=0)
        self._analyzer.source_supply_status(supply=2, status='OFF')

        self._analyzer.source_tune_dut_voltage(volt=10.5)
        self._analyzer.source_tune_dut_status('ON')

        self._analyzer.sense_adc_rosc_source(source='int')
        self._analyzer.sense_mode(mode='fn')

        # self._analyzer.send('sens:pn:freq 600k --- how to detect?')

        self._analyzer.sense_freq_start(mode='fn', freq=10000)
        self._analyzer.sense_freq_stop(mode='fn', freq=200000)
        self._analyzer.sense_freq_det(mode='fn', value='nev')

        print('*OPC?:', self._analyzer.operation_complete)

        self._analyzer.sense_corrections(mode='fn', corrections=10)
        self._analyzer.sense_averages(mode='fn', averages=1)
        self._analyzer.sense_ppd(mode='fn', value=0)
        self._analyzer.sense_spur_omis(mode='fn', omission='OFF')
        self._analyzer.sense_spur_threshold(mode='fn', threshold=10)
        self._analyzer.sense_smo_status(mode='fn', status='OFF')
        self._analyzer.sense_smo_aperture(mode='fn', aperture=1)
        self._analyzer.sense_reset(mode='fn')

        self._analyzer.trigger_init()

        self._analyzer.calc_wait_average('NEXT,800')

        # TODO implement error handling
        print('error status:', self._analyzer.system_error_all())

        self._analyzer.status_questionable_condition()

        self._analyzer.calc_prel_averages(mode='fn')
        self._analyzer.calc_prel_corrections(mode='fn')

        freqs = self._analyzer.calc_trace_freq(mode='fn')
        amps = self._analyzer.calc_trace_noise(mode='fn')
        # imag = self._analyzer.query('CALC:FN:TRAC:IMAG?')

        return freqs, amps

    @property
    def analyzer_name(self):
        return str(self._analyzer)

    @property
    def analyzer_address(self):
        return f'TCPIP::{self._ip}::inst0::INSTR'

    @analyzer_address.setter
    def analyzer_address(self, ip: str):
        self._ip = ip



