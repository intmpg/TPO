# coding=utf-8
'''
	1. �������� ��������� ����� ��� ������� calculateSquare(), calculateAngle(), isTriangle(), getType().
	2. � ��������� �� ���� ������� ���� ������, ������� ��������� ���������� ����� ������ ������ (������������ ��� ������)
	3. ��������� ������. ������ ����� ������ ��������� (� ���� ������ ������ ��).
	4. � ��������� �������� ���� �����, ���������� �� ����� ����������. ���������� ��. 
	   ��������������, ��� ������ �� ������� � ��� ���� ����� ��������.
	5. ���������� �������� �������. ��� ����� ����������� ���������� coverage https://pypi.python.org/pypi/coverage
'''

import unittest
import math

class Triangle:
	'''
		a, b, c � ������� ������������
		����� ��������� ����������, �������� �� ��� �������������
		������ ���� ���� �����������
		��������� �������� � �������
	'''
	def __init__(self, a, b, c):
		self.triangle = [a, b, c]
	
	def getA(self):
		return self.triangle[0]
		
	def getB(self):
		return self.triangle[1]
		
	def getC(self):
		return self.triangle[2]
		
	def calculatePerimeter(self):
		'''
			������ ���������
		'''
		return sum(self.triangle)
		
	def calculateSquare(self):
		'''
			������ ������� �� ������� ������
		'''
		if not(self.isTriangle()):
			return "not triangle"
		a = self.triangle[0]
		b = self.triangle[1]
		c = self.triangle[2]

		p = (a+b+c)/ 2.0
		result = (p*(p-a)*(p-b)*(p-c))
		S = math.sqrt(p*(p-a)*(p-b)*(p-c))
		return S
	
	def calculateAngle(self, angle):
		'''
			������ ���� �� ������� ���������.
			� �������� ���������� ���������� alpha, beta, gamma � �������� ����, ������� ����� ���������. 
			���� ��������� �������� ��������������� ������� (a, b, c)
			���������� �������� ���� � ��������
		'''
		a = self.triangle[0]
		b = self.triangle[1]
		c = self.triangle[2]
		
		adj1 = 1
		adj2 = 1
		adj3 = 1
		
		if (angle == 'alpha'):
			adj1 = b
			adj2 = c
			opp = a
		elif (angle == 'beta'):
			adj1 = a
			adj2 = c
			opp = b
		elif (angle == 'gamma'):
			adj1 = a
			adj2 = b
			opp = c
		else:
			return False
		if not(self.isTriangle()):
			return "not triangle"
		f = (adj1**2 + adj2**2 - opp**2)/(2.0*adj1*adj2)
		return math.degrees(math.acos(f))
	
	def isTriangle(self):
		'''
			��������, ��� ����������� � ���������� ��������� ������ ����� ������������
		'''
		a = self.triangle[0]
		b = self.triangle[1]
		c = self.triangle[2]		
		if ((a + b <= c) or (a + c <= b) or (b + c <= a)):
			return False
		else:
			return True
		
	def getType(self):
		'''
			���������� ��� ������������:
			common � ������ �����������
			isosceles � ��������������
			equilateral � ��������������
			right � �������������
		'''
		type = 'common'
		a = self.triangle[0]
		b = self.triangle[1]
		c = self.triangle[2]
		if not(self.isTriangle()):
			return "not triangle"                        
		if ((a == b) and (a == c) and(b == c)):
			type = 'equilateral'
		elif (((a == b) and (a != c)) or
                      ((a == c) and (a != b)) or
                      ((b == c) and (b != a))):
			type = 'isosceles'
		if ((a**2 == b**2 + c**2) or
                    (b**2 == a**2 + c**2) or
                    (c**2 == a**2 + b**2)):
			type = 'right'
		return type


class TriangleTest(unittest.TestCase):
	def setUp(self):
		print "Test started"
		
	def tearDown(self):
		print "Test finished"

	# ���������, ��� �� ���������� ��������� ��������� ��������
	def testIsTriangle(self):
		t = Triangle(2, 3, 4)
		self.assertTrue(t.isTriangle())
                # ����������������� ����� ������� ����(a + b <= c) or (a + c <= b) or (b + c <= a) ������� ������ ������� True
		t = Triangle(3, 3, 3)
		self.assertTrue(t.isTriangle())
                
	# �������� ������������, ��� �� �����������, ������� isTriangle() ������ ������� false
	def testIsNotTriangle(self):
		t = Triangle(2, 3, 5)
		self.assertFalse(t.isTriangle())
                #�������� ������� ������� (a + b <= c) fun = false
		t = Triangle(2, 1, 4)
		self.assertFalse(t.isTriangle())
		t = Triangle(2, 2, 4)
		self.assertFalse(t.isTriangle())
		#�������� ������� ������� (a + c <= b) fun = false
		t = Triangle(1, 2, 1)
		self.assertFalse(t.isTriangle())
		t = Triangle(1, 3, 1)
		self.assertFalse(t.isTriangle())
		#�������� �������� ������� (b + c <= a) fun = false
		t = Triangle(8, 4, 4)
		self.assertFalse(t.isTriangle())
		t = Triangle(9, 4, 4)
		self.assertFalse(t.isTriangle())

	# ���������, ��� ������ calculateSquare ������ ������ ���������
	def testCalculateSquare(self):
		t = Triangle(2, 3, 4)
		self.assertAlmostEqual(t.calculateSquare(), 2.9047375)
		
		t = Triangle(3, 3, 3)
		self.assertAlmostEqual(t.calculateSquare(), 3.89711431)
		
        # �������� ������������, ��� �������� �� ����� ��������� ������ �� ����� �����, ������� calculateSquare() ������ ������� math domain error
	def testIncorrectParamInCalculateSquare(self):
                #����� �������� � ���, ��� ��� �� ������������		
		t = Triangle(13, -3, -3)
		self.assertEqual("not triangle", t.calculateSquare())
		t = Triangle(0, 0, 0)
		self.assertEqual("not triangle", t.calculateSquare())

	# ���������, ��� ������ calculateAngle ������ ������ ���������
	def testCalculateAngle(self):
		t = Triangle(2, 3, 4)
		self.assertAlmostEqual(t.calculateAngle("alpha"), 28.9550244)
		self.assertAlmostEqual(t.calculateAngle("beta"), 46.5674634)
		self.assertAlmostEqual(t.calculateAngle("gamma"), 104.4775122)
                
        #���������, ��� ������ calculateAngle ����� ������������ �������� ����, ��������� False
	#��� ����� �������� ������� ���������� not triangle
	def testIncorrectParamInCalculateAngle(self):
                #�������� ���� �����������		
		t = Triangle(13, -3, -3)
		self.assertFalse(t.calculateAngle("a13lpasdha"))
		#�������� �������
		t = Triangle(0, 0, 0)
		self.assertEqual("not triangle", t.calculateAngle("alpha"))
		
		
	# ���������, ��� ������ getType ������ ������ ���������
	def testGetType(self):
                #������� getType ������ �������� �������������(right) ���
                #beta = 90
		t = Triangle(3, 5, 4)
		self.assertEqual("right", t.getType())
		#gamma = 90
		t = Triangle(4, 3, 5)
		self.assertEqual("right", t.getType())
                #alpha = 90
		t = Triangle(5, 3, 4)
		self.assertEqual("right", t.getType())
		#������� getType ������ �������� ��������������(isosceles) ���
		t = Triangle(3, 2, 2)
		self.assertEqual("isosceles", t.getType())
		t = Triangle(2, 2, 3)
		self.assertEqual("isosceles", t.getType())
		t = Triangle(2, 3, 2)
		self.assertEqual("isosceles", t.getType())
                #������� getType ������ �������� ��������������(equilateral) ���
		t = Triangle(3, 3, 3)
		self.assertEqual("equilateral", t.getType())
                #������� getType ������ �������� ������ �����������(common) ���
		t = Triangle(2, 3, 4)
		self.assertEqual("common", t.getType())
		# �������� ������������, ��� �� �����������, ������� getType() ������ ������� "not triangle"
		t = Triangle(0, 0, 0)
		self.assertEqual("not triangle", t.getType())
	def testGetA(self):		
		t = Triangle(13, 3, 3)
		self.assertEqual(13,t.getA())
	def testGetB(self):		
		t = Triangle(13, 3, 3)
		self.assertEqual(3,t.getB())
	def testGetC(self):		
		t = Triangle(13, 3, 3)
		self.assertEqual(3,t.getC())
	def testCalculatePerimeter(self):		
		t = Triangle(13, 3, 3)
		self.assertEqual(19, t.calculatePerimeter())
	
if __name__ == '__main__':
	unittest.main()