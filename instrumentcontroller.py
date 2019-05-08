import random

from instr.pna20 import Pna20

is_mock = False


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
            print(f'trying {self.analyzer_address}')
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

        if self._analyzer:
            self._analyzer.reset()

        return bool(self._analyzer)

    def test_sample(self):
        return True

    def new_measure(self, params):
        print(params)

        self._analyzer.reset()
        self._analyzer.source_supply_voltage(supply=1, volt=params.v1)
        self._analyzer.source_supply_status(supply=1, status='ON' if params.v1 != 0 else 'OFF')
        self._analyzer.source_supply_voltage(supply=2, volt=params.v2)
        self._analyzer.source_supply_status(supply=2, status='ON' if params.v2 != 0 else 'OFF')

        self._analyzer.source_tune_dut_voltage(volt=params.vc)
        self._analyzer.source_tune_dut_status(status='ON' if params.vc != 0 else 'OFF')

        self._analyzer.sense_adc_rosc_source(source='INT')
        self._analyzer.sense_mode(mode='FN')

        self._analyzer.sense_freq_exec()
        cur = self._analyzer.measure_supply_current(supply=1)
        amp = self._analyzer.calc_pow()
        freq = self._analyzer.calc_freq()

        print(cur)
        print(amp)
        print(freq)

    def measure(self, params):
        print(params)

        try:
            # self._analyzer.reset()
            self._analyzer.source_supply_voltage(supply=1, volt=params.v1)
            self._analyzer.source_supply_status(supply=1, status='ON' if params.v1 != 0 else 'OFF')
            self._analyzer.source_supply_voltage(supply=2, volt=params.v2)
            self._analyzer.source_supply_status(supply=2, status='ON' if params.v2 != 0 else 'OFF')

            self._analyzer.source_tune_dut_voltage(volt=params.vc)
            self._analyzer.source_tune_dut_status(status='ON' if params.vc != 0 else 'OFF')

            self._analyzer.sense_adc_rosc_source(source='INT')
            self._analyzer.sense_mode(mode='FN')

            self._analyzer.sense_freq_exec()
            cur = self._analyzer.measure_supply_current(supply=1)
            amp = self._analyzer.calc_pow()
            freq = self._analyzer.calc_freq()

            # self._analyzer.send(f'SENS:FN:FREQ {freq}')

            self._analyzer.sense_freq_start(mode='FN', freq=int(params.f1))
            self._analyzer.sense_freq_stop(mode='FN', freq=int(params.f2))
            self._analyzer.sense_freq_det(mode='FN', value='NEV')   # NEV / ALW

            self._analyzer.send(f'SENS:FN:FREQ:AUTO ON')

            print('*OPC?:', self._analyzer.operation_complete)

            self._analyzer.sense_corrections(mode='FN', corrections=params.corr)
            self._analyzer.sense_averages(mode='FN', averages=params.aver)
            self._analyzer.sense_ppd(mode='FN', value=0)
            self._analyzer.sense_spur_omis(mode='FN', omission='OFF')
            self._analyzer.sense_spur_threshold(mode='FN', threshold=10)
            self._analyzer.sense_smo_status(mode='FN', status='OFF')
            self._analyzer.sense_smo_aperture(mode='FN', aperture=1)
            self._analyzer.sense_reset(mode='FN')

            self._analyzer.trigger_init()

            self._analyzer.calc_wait_average('NEXT,800')

            self._analyzer.system_error_all()

            self._analyzer.status_questionable_condition()

            self._analyzer.calc_prel_averages(mode='FN')
            self._analyzer.calc_prel_corrections(mode='FN')

            freqs = self._analyzer.calc_trace_freq(mode='FN')
            amps = self._analyzer.calc_trace_noise(mode='FN')

            self._analyzer.system_error_all()
        except Exception as ex:
            print(ex)

        return freqs, amps, freq, amp, cur

    def ref_measure_vco_char(self):
        print('measuring VCO char')
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [random.randint(0, 10) for _ in range(10)]

    @property
    def analyzer_name(self):
        return str(self._analyzer)

    @property
    def analyzer_address(self):
        return f'TCPIP::{self._ip}::inst0::INSTR'

    @analyzer_address.setter
    def analyzer_address(self, ip: str):
        self._ip = ip



