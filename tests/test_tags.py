# Created: 21.07.2012
# License: MIT License
from __future__ import unicode_literals

import unittest
from io import StringIO

from dxfgrabber.tags import StringIterator, Tags
from dxfgrabber.tags import dxfinfo, strtag

TEST_TAGREADER = """  0
SECTION
  2
HEADER
  9
$ACADVER
  1
AC1018
  9
$DWGCODEPAGE
  3
ANSI_1252
  0
ENDSEC
  0
EOF
"""

TEST_NO_EOF = """  0
SECTION
  2
HEADER
  9
$ACADVER
  1
AC1018
  9
$DWGCODEPAGE
  3
ANSI_1252
  0
ENDSEC

"""

TEST_TAGREADER_COMMENTS = """999
Comment0
  0
SECTION
  2
HEADER
  9
$ACADVER
999
Comment1
  1
AC1018
  9
$DWGCODEPAGE
  3
ANSI_1252
  0
ENDSEC
  0
EOF
"""

class TestTagReader(unittest.TestCase):
    def setUp(self):
        self.reader = StringIterator(TEST_TAGREADER)

    def test_next(self):
        self.assertEqual((0, 'SECTION'), next(self.reader))

    def test_undo_last(self):
        self.reader.__next__()
        self.reader.undotag()
        self.assertEqual((0, 'SECTION'), next(self.reader))

    def test_error_on_multiple_undo_last(self):
        next(self.reader)
        self.reader.undotag()
        with self.assertRaises(ValueError):
            self.reader.undotag()

    def test_error_undo_last_before_first_read(self):
        with self.assertRaises(ValueError):
            self.reader.undotag()

    def test_lineno(self):
        next(self.reader)
        self.assertEqual(2, self.reader.lineno)

    def test_lineno_with_undo(self):
        next(self.reader)
        self.reader.undotag()
        self.assertEqual(0, self.reader.lineno)

    def test_lineno_with_undo_next(self):
        next(self.reader)
        self.reader.undotag()
        next(self.reader)
        self.assertEqual(2, self.reader.lineno)

    def test_to_list(self):
        tags = list(self.reader)
        self.assertEqual(8, len(tags))

    def test_undo_eof(self):
        for tag in self.reader:
            if tag == (0, 'EOF'):
                self.reader.undotag()
                break
        tag = next(self.reader)
        self.assertEqual((0, 'EOF'), tag)
        with self.assertRaises(StopIteration):
            self.reader.__next__()

    def test_no_eof(self):
        tags = list(StringIterator(TEST_NO_EOF))
        self.assertEqual(7, len(tags))
        self.assertEqual((0, 'ENDSEC'), tags[-1])

    def test_strtag_int(self):
        self.assertEqual('  1\n1\n', strtag( (1,1) ))

    def test_strtag_float(self):
        self.assertEqual(' 10\n3.1415\n', strtag( (10, 3.1415) ))

    def test_strtag_str(self):
        self.assertEqual('  0\nSECTION\n', strtag( (0, 'SECTION') ))

    def test_skip_comments(self):
        tags1 = list(StringIterator(TEST_TAGREADER))
        tags2 = list(StringIterator(TEST_TAGREADER_COMMENTS))
        self.assertEqual(tags1, tags2)


class TestGetDXFInfo(unittest.TestCase):
    def test_dxfinfo(self):
        info = dxfinfo(StringIO(TEST_TAGREADER))
        self.assertEqual(info.release, 'R2004')
        self.assertEqual(info.encoding, 'cp1252')

TESTHANDLE5 = """ 0
TEST
  5
F5
"""

TESTHANDLE105 = """ 0
TEST
105
F105
"""

TESTFINDALL = """  0
TEST0
  0
TEST1
  0
TEST2
"""

POINT_2D_TAGS = """ 10
100
 20
200
  9
check mark 1
 10
100
 20
200
 30
300
  9
check mark 2
"""


class TestTags(unittest.TestCase):
    def setUp(self):
        self.tags = Tags.fromtext(TEST_TAGREADER)

    def test_from_text(self):
        self.assertEqual(8, len(self.tags))

    def test_write(self):
        stream = StringIO()
        self.tags.write(stream)
        result = stream.getvalue()
        stream.close()
        self.assertEqual(TEST_TAGREADER, result)

    def test_update(self):
        self.tags.update(2, 'XHEADER')
        self.assertEqual('XHEADER', self.tags[1].value)

    def test_update_error(self):
        with self.assertRaises(ValueError):
            self.tags.update(999, 'DOESNOTEXIST')

    def test_findall(self):
        tags = Tags.fromtext(TESTFINDALL)
        self.assertEqual(3, len(tags.findall(0)))

    def test_tagindex(self):
        tags = Tags.fromtext(TESTFINDALL)
        index = tags.tagindex(0)
        self.assertEqual(0, index)
        index = tags.tagindex(0, index+1)
        self.assertEqual(1, index)

    def test_findfirst_value_error(self):
        tags = Tags.fromtext(TESTFINDALL)
        with self.assertRaises(ValueError):
            tags.tagindex(1)

    def test_read_2D_points(self):
        stri = StringIterator(POINT_2D_TAGS)
        tags = list(stri)
        self.assertEqual(15, stri.lineno)  # 14 lines
        tag = tags[0]  # 2D point
        self.assertEqual((100, 200), tag.value)
        tag = tags[1]  # check mark
        self.assertEqual('check mark 1', tag.value)
        tag = tags[2]  # 3D point
        self.assertEqual((100, 200, 300), tag.value)
        tag = tags[3]  # check mark
        self.assertEqual('check mark 2', tag.value)

DUPLICATETAGS = """  0
FIRST
  0
LAST
  1
TEST2
"""
