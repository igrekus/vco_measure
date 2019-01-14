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
        print(f'measuring {params}')
        time.sleep(1)
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 8, 6, 5, 4, 3, 2, 1.8, 1.5, 1.3]

    @property
    def analyzer_name(self):
        return str(self._analyzer)

    @property
    def analyzer_address(self):
        return f'TCPIP::{self._ip}::inst0::INSTR'

    @analyzer_address.setter
    def analyzer_address(self, ip: str):
        self._ip = ip



