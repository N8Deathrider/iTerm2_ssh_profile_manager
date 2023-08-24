import json
import unittest
from manager import Profiles
from pathlib import Path


class ProfilesTester(unittest.TestCase):

    json_file_path = None
    non_json_file_path = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.json_file_path = Path.home().joinpath("iTerm2_dynamic_profiles_test_file.json")
        with cls.json_file_path.open("w") as fp:
            json.dump({"Profiles": [{"Command": "/usr/bin/ssh username@127.0.0.1"}]}, fp)
        cls.non_json_file_path = Path.home().joinpath("iTerm2_dynamic_profiles_test_file.text")
        with cls.non_json_file_path.open("w") as _:
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass
        cls.json_file_path.unlink()
        cls.non_json_file_path.unlink()

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_ssh_path(self):
        profiles_manager = Profiles(profiles_file=self.json_file_path)
        self.assertEqual(profiles_manager._ssh_path, "/usr/bin/ssh")

    def test_init_file_errors(self):
        with self.assertRaises(FileNotFoundError):
            Profiles(profiles_file="/")

        with self.assertRaises(TypeError):
            Profiles(profiles_file=self.non_json_file_path)

        with self.assertRaises(Exception):
            Profiles(profiles_file="")

    def test_get_existing_profiles(self):
        profiles = Profiles(profiles_file=self.json_file_path)
        self.assertSetEqual({"127.0.0.1"}, profiles.existing_profiles)


if __name__ == '__main__':
    unittest.main()
