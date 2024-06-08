import unittest
import os
import shutil

# Import the function to be tested
from ocr_toolkits.change_files_ext import change_files_ext

class TestChangeFilesExt(unittest.TestCase):

    def setUp(self):
        """
        Set up a temporary directory structure for testing.
        """
        self.test_src_dir = 'src'
        self.test_dst_dir = 'dst'
        self.target_ext = '.jpg'
        
        # Create source and destination directories
        os.makedirs(self.test_src_dir, exist_ok=True)
        os.makedirs(self.test_dst_dir, exist_ok=True)
        
        # Create test files in the source directory
        self.test_files = ['test1.png', 'test2.png', 'test3.png']
        for file in self.test_files:
            with open(os.path.join(self.test_src_dir, file), 'w') as f:
                f.write('test content')

    def tearDown(self):
        """
        Clean up the temporary directories after testing.
        """
        shutil.rmtree(self.test_src_dir)
        shutil.rmtree(self.test_dst_dir)

    def test_change_files_ext(self):
        """
        Test the change_files_ext function.
        """
        # Call the function to change file extensions
        change_files_ext(self.test_src_dir, self.test_dst_dir, self.target_ext)
        
        # Verify the files in the destination directory have the correct extension
        for file in self.test_files:
            base, _ = os.path.splitext(file)
            expected_file = base + self.target_ext
            self.assertTrue(os.path.exists(os.path.join(self.test_dst_dir, expected_file)))

        # Verify the content of the files to ensure they are copied correctly
        for file in self.test_files:
            base, _ = os.path.splitext(file)
            expected_file = base + self.target_ext
            with open(os.path.join(self.test_dst_dir, expected_file), 'r') as f:
                content = f.read()
                self.assertEqual(content, 'test content')

if __name__ == '__main__':
    unittest.main()
