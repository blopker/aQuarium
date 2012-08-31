import aquarium
from aquarium import utils
import unittest
from collections import OrderedDict


class AquariumTestCase(unittest.TestCase):

    def setUp(self):
        aquarium.app.config['AQ_DIR'] = 'test_dir'
        self.app = aquarium.app.test_client()

    def test_index(self):
        resp = self.app.get('/')
        assert "logs" in resp.data
        assert "info" in resp.data
        assert "USER" in resp.data

    def test_tabularToDict(self):
        data = "bo is awesome\n1 2 3\n4 5 6"
        dic = OrderedDict([("bo", ("1", "4")), ("is", ("2", "5")), ("awesome", ("3", "6"))])
        assert utils.tabularToDict(data) == dic


class LogsTestCase(unittest.TestCase):
    """Tests for the built in logs section"""
    def setUp(self):
        aquarium.app.config['AQ_DIR'] = 'test_dir'
        self.app = aquarium.app.test_client()

    def test_log(self):
        log = "vmstat.log"
        resp = self.app.get("logs/" + log)
        assert "bo" in resp.data

    def test_logs(self):
        resp = self.app.get('logs/')
        assert "vmstat.log" in resp.data


class InfoTestCase(unittest.TestCase):
    """Tests for the built in info section"""
    def setUp(self):
        aquarium.app.config['AQ_DIR'] = 'test_dir'
        self.app = aquarium.app.test_client()

    def test_info_index(self):
        resp = self.app.get('info/')
        assert "ps.sh" in resp.data
        resp = self.app.get('info/ps.sh')
        assert "bo" in resp.data

    def test_info(self):
        script = 'not_a_real_info'
        resp = self.app.get('info/' + script)
        assert resp.status_code == 404
        script = 'fail.sh'
        resp = self.app.get('info/' + script)
        assert "command not found" in resp.data

    def test_isinfo(self):
        assert utils.isScript('info/ps.sh') == True


class ControlsTestCase(unittest.TestCase):
    """Tests for Controls"""
    def setUp(self):
        aquarium.app.config['AQ_DIR'] = 'test_dir'
        self.app = aquarium.app.test_client()

    def test_controls_index(self):
        resp = self.app.get('controls/')
        assert 'controls' in resp.data
        assert 'sleep' in resp.data

    def test_control(self):
        resp = self.app.post('/controls/nsman/start.sh')
        print resp.data
        assert 'started' in resp.data

if __name__ == '__main__':
    unittest.main()
