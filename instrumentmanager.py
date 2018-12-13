import asyncio
import sys
import time
import openpyxl
import visa

from os import listdir
from os.path import isfile, join

# TODO: write class for PNA20
from analyzer import Analyzer
from analyzermock import AnalyzerMock

# MOCK
mock_enabled = True


class InstrumentManager(object):

    def __init__(self, address='TCPIP::169.254.9.227::inst0::INSTR'):
        super().__init__()
        print('instrument manager: init')

        self._address = address
        self._analyzer: AnalyzerMock = None
        self._samplePresent = False

        self._captions = ['freq', 'amp']

        self._measure_data = list()

    def findInstruments(self):
        print('instrument manager: find instruments')
        print('searching LAN...')

        def find_live(addr):
            # TODO refactor this mess
            rm = visa.ResourceManager()
            try:
                inst = rm.open_resource(addr)
                answer = inst.query('*IDN?')
                model = answer.split(',')[1].strip()
                if model == 'PNA20':
                    self._analyzer = Analyzer(addr, answer, inst)
            except Exception as ex:
                print(ex)

        def find_mocks():
            print(self._address)
            self._analyzer = AnalyzerMock(address=self._address, idn=',PNA20 mock,')

        if mock_enabled:
            find_mocks()
        else:
            find_live(self._address)

        return self._analyzer is not None

    def getInstrumentNames(self):
        return self._analyzer.name

    def checkSample(self):
        print('instrument manager: check sample')

        if isfile('settings.ini'):
            with open('settings.ini') as f:
                line = f.readline()
                self.pow_limit = float(line.split('=')[1].strip())

        print('performing check sample algorithm')
        if not mock_enabled:
            time.sleep(1)

        self._analyzer.set_autocalibrate('OFF')
        self._analyzer.read_pow(1)

        self._samplePresent = True

        self._analyzer.set_system_local()

        return self._samplePresent

    def measure(self, params):
        print(f'instrument manager: start measure {params}')

        self._measure_data = list()
        self.measureTask()

        print('instrument manager: end measure')

    def measureTask(self):
        print(f'measurement task run')

        self._analyzer.set_autocalibrate('OFF')
        self._analyzer.set_span(10, 'MHz')
        self._analyzer.set_marker_mode(1, 'POS')

        time.sleep(0.2)
        self._measure_data = [
            [1, 1],
            [2, 2],
            [3, 3]
        ]

        self._analyzer.set_autocalibrate('ON')
        self._analyzer.set_system_local()
