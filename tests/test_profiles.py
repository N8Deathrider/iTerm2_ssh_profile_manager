import unittest
import json
from pathlib import Path
from unittest.mock import patch
from profile_manager import Profiles


class TestProfiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the test_profiles.json file
        test_data = {"Profiles": []}
        with Path("test_profiles.json").open("w") as f:
            json.dump(test_data, f)

        # Create the logs directory
        Path("logs").mkdir()

        # Set up the instance of Profiles needed for the tests modifying the data
        cls.profiles = Profiles("test_profiles.json")

    @classmethod
    def tearDownClass(cls):
        # Clean up any resources used in the tests
        Path("test_profiles.json").unlink()
        Path("logs").rmdir()

    def test_init_existing_file(self):
        # Test initializing with an existing JSON file
        self.assertTrue(self.profiles.data)

    def test_init_nonexistent_file(self):
        # Test initializing with a non-existent JSON file

        # Simulate user input of "n" for the prompt
        with patch("builtins.input", side_effect=["n"]):
            with self.assertRaises(FileNotFoundError):
                Profiles("nonexistent.json")

    def test_init_non_file_path(self):
        # Test initializing with a path that is not a file
        with self.assertRaises(IsADirectoryError):
            Profiles("logs")

    def test_init_non_json_extension(self):
        # Test initializing with a file that doesn't have a .json extension
        Path("test_profiles.txt").touch()

        with self.assertRaises(TypeError):
            Profiles("test_profiles.txt")

        Path("test_profiles.txt").unlink()

    def test_add_profile(self):
        # Test adding a profile
        self.profiles.add_profile("user", "profile1", "127.0.0.1", ["tag1"], "logs", auto_write=False)
        self.assertEqual(len(self.profiles.data["Profiles"]), 1)

    def test_delete_profiles(self):
        # Test deleting a profile
        self.profiles.add_profile("user", "profile2", "192.168.0.1", ["tag2"], "logs", auto_write=False)
        deleted_profile = self.profiles.delete_profile("192.168.0.1")
        self.assertEqual(deleted_profile["Name"], "profile2")

    def test_get_profile_values(self):
        # Test getting the arguments that are needed to create a profile using the add_profile method
        control = ("user", "profile3", "192.168.0.2", ["tag1", "tag2", "tag3"],
                   str(Path("logs").resolve()), "description")
        self.profiles.add_profile(*control, auto_write=False)
        profile = self.profiles.delete_profile(control[2])
        result = self.profiles.get_parameters(profile)
        self.assertTupleEqual(control, result)


if __name__ == "__main__":
    unittest.main()
