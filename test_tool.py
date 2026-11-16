import unittest
from tool import strip_metadata, inspect_segments
class ExifTests(unittest.TestCase):
    def test_removes_exif_and_comment(self):
        data=b"\xff\xd8\xff\xe1\x00\x06EXIF\xff\xfe\x00\x04hi\xff\xda\x00\x02scan\xff\xd9"
        cleaned,removed=strip_metadata(data)
        self.assertNotIn(b"EXIF",cleaned); self.assertIn(b"scan",cleaned)
        self.assertEqual(len(removed),2)
    def test_preserves_app0(self):
        data=b"\xff\xd8\xff\xe0\x00\x04ab\xff\xd9"
        self.assertEqual(strip_metadata(data)[0],data)
    def test_rejects_non_jpeg(self):
        with self.assertRaises(ValueError): inspect_segments(b"not jpeg")
if __name__=="__main__": unittest.main()
