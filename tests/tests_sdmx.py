import unittest
import simpledmx
from pandasdmx.api import Request


class SDMXTestCase(unittest.TestCase):
    def setUp(self):
        self.sources = list_sdmx_sources()
        self.sessions = get_sessions(sources=self.sources)

    def test_sessions_dict(self):
        self.assertIsInstance(self.sessions, dict)

    def test_sessions_ABS(self):
        self.assertIsInstance(self.sessions["ABS"], Request)

    def test_sessions_BBK(self):
        self.assertIsInstance(self.sessions["BBK"], Request)

    def test_sessions_BIS(self):
        self.assertIsInstance(self.sessions["BIS"], Request)

    def test_sessions_ECB(self):
        self.assertIsInstance(self.sessions["ECB"], Request)

    def test_sessions_ESTAT(self):
        self.assertIsInstance(self.sessions["ESTAT"], Request)

    def test_sessions_ILO(self):
        self.assertIsInstance(self.sessions["ILO"], Request)

    def test_sessions_IMF(self):
        self.assertIsInstance(self.sessions["IMF"], Request)

    def test_sessions_INEGI(self):
        self.assertIsInstance(self.sessions["INEGI"], Request)

    def test_sessions_INSEE(self):
        self.assertIsInstance(self.sessions["INSEE"], Request)

    def test_sessions_ISTAT(self):
        self.assertIsInstance(self.sessions["ISTAT"], Request)

    def test_sessions_LSD(self):
        self.assertIsInstance(self.sessions["LSD"], Request)

    def test_sessions_NB(self):
        self.assertIsInstance(self.sessions["NB"], Request)

    def test_sessions_NBB(self):
        self.assertIsInstance(self.sessions["NBB"], Request)

    def test_sessions_OECD(self):
        self.assertIsInstance(self.sessions["OECD"], Request)

    def test_sessions_SGR(self):
        self.assertIsInstance(self.sessions["SGR"], Request)

    def test_sessions_SPC(self):
        self.assertIsInstance(self.sessions["SPC"], Request)

    def test_sessions_STAT_EE(self):
        self.assertIsInstance(self.sessions["STAT_EE"], Request)

    def test_sessions_UNSD(self):
        self.assertIsInstance(self.sessions["UNSD"], Request)

    def test_sessions_UNICEF(self):
        self.assertIsInstance(self.sessions["UNICEF"], Request)

    def test_sessions_CD2030(self):
        self.assertIsInstance(self.sessions["CD2030"], Request)

    def test_sessions_WB(self):
        self.assertIsInstance(self.sessions["WB"], Request)

    def test_sessions_WB_WDI(self):
        self.assertIsInstance(self.sessions["WB_WDI"], Request)
