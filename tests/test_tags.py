# Created: 21.07.2012
# License: MIT License
from __future__ import unicode_literals

import unittest
from io import StringIO
import math

from dxfgrabber.tags import Tags, DXFTag, string_tagger
from dxfgrabber.tags import dxfinfo, to_float_with_infinite

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
        self.reader = string_tagger(TEST_TAGREADER)

    def test_next(self):
        self.assertEqual(DXFTag(0, 'SECTION'), next(self.reader))

    def test_to_list(self):
        tags = list(self.reader)
        self.assertEqual(8, len(tags))

    def test_no_eof(self):
        tags = list(string_tagger(TEST_NO_EOF))
        self.assertEqual(7, len(tags))
        self.assertEqual(DXFTag(0, 'ENDSEC'), tags[-1])

    def test_skip_comments(self):
        tags1 = list(string_tagger(TEST_TAGREADER))
        tags2 = list(string_tagger(TEST_TAGREADER_COMMENTS))
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
        self.tags = Tags.from_text(TEST_TAGREADER)

    def test_from_text(self):
        self.assertEqual(8, len(self.tags))

    def test_findall(self):
        tags = Tags.from_text(TESTFINDALL)
        self.assertEqual(3, len(tags.find_all(0)))

    def test_tagindex(self):
        tags = Tags.from_text(TESTFINDALL)
        index = tags.tag_index(0)
        self.assertEqual(0, index)
        index = tags.tag_index(0, index+1)
        self.assertEqual(1, index)

    def test_findfirst_value_error(self):
        tags = Tags.from_text(TESTFINDALL)
        with self.assertRaises(ValueError):
            tags.tag_index(1)

    def test_read_2D_points(self):
        stri = string_tagger(POINT_2D_TAGS)
        tags = list(stri)
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

XDATA = """0
LINE
5
1
330
2
102
{DXFGrabber
330
999
102
}
10
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
1001
DXFGRABBER
1000
XDATA_STRING
"""


class TestXData(unittest.TestCase):
    def setUp(self):
        self.tags = Tags.from_text(XDATA)

    def test_get_xdata(self):
        xdata = self.tags.xdata()
        self.assertEqual([(1001, 'DXFGRABBER'), (1000, 'XDATA_STRING')], xdata)

class TestAppData(unittest.TestCase):
    def setUp(self):
        self.tags = Tags.from_text(XDATA)

    def test_get_app_data(self):
        app_data = self.tags.app_data()
        self.assertEqual([(102, '{DXFGrabber'), (330, '999'), (102, '}')], app_data['{DXFGrabber'])

    def test_plain_tags(self):
        plain_tags = list(self.tags.plain_tags())
        self.assertEqual(7, len(plain_tags))  # coords like 10, 20, 30 are just one tag (10, (x,y,z))

ELLIPSE = """  0
ELLIPSE
  5
3D2
330
1F
100
AcDbEntity
  8
0
100
AcDbEllipse
 10
0.0
 20
0.0
 30
0.0
 11
2.60
 21
1.50
 31
0.0
210
0.0
220
0.0
230
1.0
 40
0.33
 41
0.0
 42
6.28
"""


class TestSubclasses(unittest.TestCase):
    def setUp(self):
        self.tags = Tags.from_text(ELLIPSE)

    def test_subclasses(self):
        subclasses = self.tags.subclasses()
        self.assertEqual(3, len(subclasses))
        self.assertEqual(3, len(subclasses['noname']))
        self.assertEqual(1, len(subclasses['AcDbEntity']))
        self.assertEqual(6, len(subclasses['AcDbEllipse']))


class TestInfinite(unittest.TestCase):
    def test_to_float(self):
        self.assertEqual(1.0, to_float_with_infinite('1.0'))
        with self.assertRaises(ValueError):
            to_float_with_infinite('abc')

    def test_infinite(self):
        self.assertTrue(math.isinf(to_float_with_infinite(' -inf.0  ')))
        self.assertTrue(math.isinf(to_float_with_infinite(' INF.0  ')))