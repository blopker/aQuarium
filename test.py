import aquarium
import unittest
import json
from collections import OrderedDict


class AquariumTestCase(unittest.TestCase):

    def setUp(self):
        aquarium.app.config['SCRIPTS'] = 'test_scripts'
        self.app = aquarium.app.test_client()

    def test_index(self):
        resp = self.app.get('/')
        assert "Welcome" in resp.data
        assert "fail" in resp.data
        assert "uname" in resp.data
        assert "ps" in resp.data

    def test_script(self):
        script = 'not_a_real_script'
        resp = self.app.get('script/' + script)
        assert resp.status_code == 501

        script = 'uname.sh'
        resp = self.app.get('script/' + script)
        assert "Linux" in resp.data

        script = 'ps.sh'
        resp = self.app.get('script/' + script)
        assert "root" in resp.data

        script = 'fail.sh'
        resp = self.app.get('script/' + script)
        assert resp.status_code == 500

    def test_logs(self):
        log = "vmstat.log"
        resp = self.app.get("log/" + log)
        assert "bo" in resp.data

    def test_logFormat(self):
        data = "bo is awesome\n1 2 3\n4 5 6"
        dic = OrderedDict([("bo", ("1", "4")), ("is", ("2", "5")), ("awesome", ("3", "6"))])
        assert aquarium.formatLog(data) == dic

    def test_getScripts(self):
        lis = aquarium.getScripts()
        assert "ps.sh" in lis
        assert "not_executable" not in lis

if __name__ == '__main__':
    unittest.main()
