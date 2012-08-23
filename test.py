import aquarium
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

    def test_scripts(self):
        resp = self.app.get('scripts/')
        assert "ps.sh" in resp.data

    def test_logs(self):
        resp = self.app.get('logs/')
        assert "vmstat.log" in resp.data

    def test_script(self):
        script = 'not_a_real_script'
        resp = self.app.get('scripts/' + script)
        assert resp.status_code == 501

    #     script = 'uname.sh'
    #     resp = self.app.get('script/' + script)
    #     assert "Linux" in resp.data

    #     script = 'ps.sh'
    #     resp = self.app.get('script/' + script)
    #     assert "root" in resp.data

    #     script = 'fail.sh'
    #     resp = self.app.get('script/' + script)
    #     assert resp.status_code == 500

    def test_log(self):
        log = "vmstat.log"
        resp = self.app.get("logs/" + log)
        assert "bo" in resp.data

    def test_tabularToDict(self):
        data = "bo is awesome\n1 2 3\n4 5 6"
        dic = OrderedDict([("bo", ("1", "4")), ("is", ("2", "5")), ("awesome", ("3", "6"))])
        assert aquarium.views.tabularToDict(data) == dic

    # def test_getDirs(self):
    #     dirs, files = aquarium.views.getContents("")
    #     assert "logs" in dirs
    #     assert "scripts" in dirs

    #     dirs, files = aquarium.views.getContents("logs/")
    #     assert "vmstat.log" in files

if __name__ == '__main__':
    unittest.main()
