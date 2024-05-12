import unittest
from problem1 import *

class TestProblem1(unittest.TestCase):
  def test_anagram1(self):
    result = main("race")
    print(result)
    self.assertEqual(result, ['acre', 'care', 'cera', 'race'])
  
  #アナグラムがない場合
  def test_anagram2(self):
    result = main("az")
    print(result)
    self.assertEqual(result, None)
  
  #アナグラムが短い時
  def test_anagram3(self):
    result = main("a")
    print(result)
    self.assertEqual(result, ['a'])
  
  #アナグラムが長い時
  def test_anagram4(self):
    result = main("abfewgrwghtrhrtj")
    print(result)
    self.assertEqual(result, None)
  
  #空白の入力の時
  def test_anagram5(self):
    result = main("")
    print(result)
    self.assertEqual(result, None)
  
if __name__ == '__main__':
  unittest.main()