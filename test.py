import aquarium
from aquarium.sections import scripts
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
        assert "scripts" in resp.data
        assert "imapeanutbutter" in resp.data

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


class ScriptsTestCase(unittest.TestCase):
    """Tests for the built in scripts section"""
    def setUp(self):
        aquarium.app.config['AQ_DIR'] = 'test_dir'
        self.app = aquarium.app.test_client()

    def test_scripts(self):
        resp = self.app.get('scripts/')
        assert "ps.sh" in resp.data
        resp = self.app.get('scripts/ps.sh')
        assert "bo" in resp.data

    def test_script(self):
        script = 'not_a_real_script'
        resp = self.app.get('scripts/' + script)
        assert resp.status_code == 404
        script = 'fail.sh'
        resp = self.app.get('scripts/' + script)
        assert "command not found" in resp.data

    def test_isScript(self):
        assert scripts.isScript('scripts/ps.sh') == True


class NsmanTestCase(unittest.TestCase):
    """Tests for NSman"""
    def setUp(self):
        aquarium.app.config['AQ_DIR'] = 'test_dir'
        self.app = aquarium.app.test_client()

    def test_nsman_index(self):
        resp = self.app.get('nsman/')
        assert 'nsman' in resp.data

if __name__ == '__main__':
    unittest.main()
