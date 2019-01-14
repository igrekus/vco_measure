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
        # time.sleep(1)

        # *IDN?
        # *TST
        # conf:nois:boar a
        # diag:lic:read?
        # sens:mode?
        # sens:mode intn
        # sens:pn:puls off; sens:pn:aver?
        # sens:pn:corr?
        # sens:pn:ref?
        # sens:pn:freq:star?
        # sens:pn:freq:stop?
        # syst:comm:lan:mac?
        # conf:nois:boar b
        # sour:fm:sens?
        # conf:nois:boar a
        # sour:fm:sens?
        # sens:pn:ref?
        # sour:tune:ref1:min?
        # sour:tune:ref1:max?
        # sour:tune:ref2:min?
        # sour:tune:ref2:max?
        # sens:pn:ref1:sens?
        # sens:pn:ref2:sens?
        # diag:pn:fd:stag? max
        # sour:supp1:volt? min
        # sour:supp1:volt? max
        # sour:supp1:volt?
        # sour:supp2:volt?
        # sour:supp1:stat?
        # sour:supp2:stat?
        # sour:tune:dut:volt?
        # sour:tune:dut:stat?
        # diag:cal:read?

        # syst:comm:lan:rtm 0 10
        # sens:mode fn
        # sens:pn:puls off
        # sens:fn:aver?
        # sens:fn:corr?
        # sens:fn:freq:star?
        # sens:fn:freq:stop?
        # meas:supp1:curr?
        # sens:freq:exec
        # syst:err:all?
        # calc:freq?
        # calc:pow?
        # syst:err:all?
        # sens:fn:freq? max
        # sens:pn:freq? max
        # conf:nois:boar a
        # diag:pn:vtun?
        # conf:nois:boar b
        # diag:pn:vtun?
        # meas:supp1:curr?

        # sour:supp1:stat on
        # sour:supp1:volt 4.5

        # sens:adc:rosc:sour int
        # sens:mode fn; sens:fn:freq xxxxx; sens:fn:freq:star xxxx; sens:fn:freq:stop xxxx; sens:fn:freq:det nev; *opc?
        # sens:fn:freq:auto off

        # ---

        # sour:supp1:stat on
        # sour:supp1:volt 4.5
        # sour:supp2:stat off
        # sour:supp2:volt 0

        # sens:adc:rosc:sour int
        # sens:mode fn
        # sens:fn:freq 600k --- how to detect?
        # sens:fn:freq:star 10
        # sens:fn:freq:stop 1000000
        # sens:fn:freq:det nev
        # *opc?
        # SENS:FN:CORR 1
        # SENS:FN:AVER 1
        # SENS:FN:PPD 0
        # SENS:FN:SPUR:OMIS OFF
        # SENS:FN:SPUR:THR 10
        # SENS:FN:SMO:STAT OFF
        # SENS:FN:SMO:APER 1
        # SENS:FN:RES

        # INIT

        # CALC:WAIT:AVER NEXT,800
        # SYST:ERR:ALL?
        # STAT:QUES:POW:COND?
        # CALC:FN:PREL:AVER?
        # CALC:FN:PREL:CORR?
        # CALC:FN:TRAC:FREQ?
        # CALC:FN:TRAC:NOIS?
        # CALC:FN:TRAC:IMAG?


        # ===

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



