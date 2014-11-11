import unittest
from gmond import GmondCollector

class GmondCollectorTests(unittest.TestCase):

  def test_max_age_limit_of_user_processes(self):
    self.maxDiff = None
    self.assertEqual({}, GmondCollector().get_hosts_with_outdated_processes())

if __name__ == '__main__':
  unittest.main()

