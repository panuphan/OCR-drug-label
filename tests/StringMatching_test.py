import unittest
from src.StringMatching import *

# run code command:
# python -m unittest tests/StringMatching_test.py

class StringMatchingTest(unittest.TestCase):
    def setUp(self):
        self.true_dict_list=[
          ({"name":"นาง สุวิภา อยู่สุข","ID":"HN43218","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43211","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาง สุวิภา อยู่สุข","ID":"HN43882","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43  2","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาสุวิา  อยสุข","ID":"HN48211","date":"2412/63","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43211","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาง สุวิภา อยู่สุข","ID":"HN43882","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43833","date":"23/02/63","tmp1":"tmp1"}),
        ]

        self.false_dict_list=[
          ({"name":"นาย กลม แซ่ตั้ง","ID":"HN43218","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43211","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาย กลม แซ่ตั้ง","ID":"HN43218","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นาย สวัสดี อยุสข","ID":"HN43411","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาย กลม แซ่ตั้ง","ID":"HN48211","date":"2412/63","tmp1":"tmp1"},
          {"name":"นา ขแบเขต บุญมี","ID":"Hห43211","date":"2412/63","tmp1":"tmp1"}),

          ({"name":"นาย กลม แซ่ตั้ง","ID":"HN43854","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นาง กลมวัลย์ แซ่ตั้ง","ID":"HN46831","date":"24/03/63","tmp1":"tmp1"}),

          ({"name":"นางสุวณสีย์ เที่ยงแท้","ID":"HN4485","date":"22/02/62","tmp1":"tmp1"},
          {"name":"นางทองประสม เที่ยงแท้","ID":"HN4481","date":"23/02/62","tmp1":"tmp1"}),

          ({"name":"นาง กมล บางเลน","ID":"HN43825","date":"23/02/63","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43211","date":"23/02/63","tmp1":"tmp1"}),
        ]


    def test_true_dict75(self):
        result = [StringMatching(75,qr,ocr,["name","ID","date"],True) for qr,ocr in self.true_dict_list]
        act = [True for _ in range(len(self.true_dict_list))]
        msg = "<<< actual ERROR:test_true_dict75"
        # self.assertEqual(result, act, msg)
        self.assertSequenceEqual(result, act,msg)
    
    def test_false_dict75(self):
        result = [StringMatching(75,qr,ocr,["name","ID","date"]) for qr,ocr in self.false_dict_list]
        act = [False for _ in range(len(self.false_dict_list))]
        msg = "<<< actual ERROR:test_false_dict75"
        # self.assertEqual(result, act, msg)
        self.assertSequenceEqual(result, act,msg)


if __name__ == '__main__':
    unittest.main()
