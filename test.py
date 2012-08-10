import aquarium
import unittest


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
        resp = self.app.get('/' + script)
        assert resp.status_code == 501

        script = 'uname'
        resp = self.app.get('/' + script)
        assert "Linux" in resp.data

        script = 'ps'
        resp = self.app.get('/' + script)
        assert "root" in resp.data

        script = 'fail'
        resp = self.app.get('/' + script)
        assert resp.status_code == 500

    def test_nav(self):
        resp = self.app.get("/commands", follow_redirects=True)
        assert "/ps" in resp.data

    def test_getCommands(self):
        lis = aquarium.getCommands()
        assert "ps" in lis
        assert "not_executable" not in lis

if __name__ == '__main__':
    unittest.main()
