import unittest
from queue import Queue
import shutil

from bears.general.ImageDimensionBear import ImageDimensionBear
from coalib.settings.Section import Section


class ImageDimensionBearTest(unittest.TestCase):
    """
    Runs unittests for ImageDimensionBear
    """

    def setUp(self):
        self.section = Section('')
        self.queue = Queue()
        self.file_dict = {}
        self.idb = ImageDimensionBear(None, self.section, self.queue)

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(ImageDimensionBear.check_prerequisites(),
                             'img_checker is not installed.')

            shutil.which = lambda *args, **kwargs: 'path/to/git'
            self.assertTrue(ImageDimensionBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which    

    def test_run_with_png(self):
        message = "message='The image ./test-img/img.png is larger"
        message += " than 240px x 240px [w x h]'"
        self.assertIn(message,
                      str(list(self.idb.run(
                               image_file='./test-img/*.png',
                               width=240,
                               height=240))))

    def test_run_with_jpg(self):
        self.assertEqual('[]',
                         str(list(self.idb.run(
                                  image_file='./test-img/*.jpg',
                                  width=240,
                                  height=240))))

    def test_run_with_jpg_fail(self):
        message = "message='The image ./test-img/images.jpg is larger"
        message += " than 50px x 50px [w x h]'"
        self.assertIn(message,
                      str(list(self.idb.run(
                               image_file='./test-img/*.jpg',
                               width=50,
                               height=50))))

    def test_run_with_both(self):
        message_png = "message='The image ./test-img/img.png is larger"
        message_png += " than 50px x 50px [w x h]'"
        message_jpg = "message='The image ./test-img/images.jpg is larger"
        message_jpg += " than 50px x 50px [w x h]'"
        output = str(list(self.idb.run(image_file='./test-img/*.*',
                                       width=50,
                                       height=50)))
        self.assertIn(message_png,
                      output)
        self.assertIn(message_jpg,
                      output)
