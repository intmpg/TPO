# coding=utf-8
'''
	1. Напишите модульные тесты для функций calculateSquare(), calculateAngle(), isTriangle(), getType().
	2. В некоторых из этих функций есть ошибки, поэтому правильно написанные тесты должны падать (обнаруживать эти ошибки)
	3. Исправьте ошибки. Теперь тесты должны проходить (у всех тестов статус ОК).
	4. В указанных функциях есть места, написанные не очень эффективно. Перепишите их. 
	   Удостоверьтесь, что ничего не сломано — все ваши тесты проходят.
	5. Посчитайте покрытие тестами. Для этого используйте инструмент coverage https://pypi.python.org/pypi/coverage
'''

import unittest
import math

class Triangle:
	'''
		a, b, c — стороны треугольника
		класс позволяет определить, является ли это треугольником
		какого типа этот треугольник
		посчитать периметр и площадь
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
			расчет периметра
		'''
		return sum(self.triangle)
		
	def calculateSquare(self):
		'''
			расчет площади по формуле Герона
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
			Расчет угла по теореме косинусов.
			В качестве параметров передается alpha, beta, gamma — название угла, который нужно посчитать. 
			Угол находится напротив соответствующей стороны (a, b, c)
			Возвращает величину угла в градусах
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
			Проверка, что треугольник с введенными сторонами вообще может существовать
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
			Возвращает тип треугольника:
			common — просто треугольник
			isosceles — равнобедренный
			equilateral — равносторонний
			right — прямоугольный
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

	# Проверяем, что на корректных значениях программа работает
	def testIsTriangle(self):
		t = Triangle(2, 3, 4)
		self.assertTrue(t.isTriangle())
                # неудовлетворяющий этому условию тест(a + b <= c) or (a + c <= b) or (b + c <= a) функция должна вернуть True
		t = Triangle(3, 3, 3)
		self.assertTrue(t.isTriangle())
                
	# значение некорректное, это не треугольник, функция isTriangle() должна вернуть false
	def testIsNotTriangle(self):
		t = Triangle(2, 3, 5)
		self.assertFalse(t.isTriangle())
                #проверка первого условия (a + b <= c) fun = false
		t = Triangle(2, 1, 4)
		self.assertFalse(t.isTriangle())
		t = Triangle(2, 2, 4)
		self.assertFalse(t.isTriangle())
		#проверка второго условия (a + c <= b) fun = false
		t = Triangle(1, 2, 1)
		self.assertFalse(t.isTriangle())
		t = Triangle(1, 3, 1)
		self.assertFalse(t.isTriangle())
		#проверка третьего условия (b + c <= a) fun = false
		t = Triangle(8, 4, 4)
		self.assertFalse(t.isTriangle())
		t = Triangle(9, 4, 4)
		self.assertFalse(t.isTriangle())

	# Проверяем, что фунция calculateSquare выдает верный результат
	def testCalculateSquare(self):
		t = Triangle(2, 3, 4)
		self.assertAlmostEqual(t.calculateSquare(), 2.9047375)
		
		t = Triangle(3, 3, 3)
		self.assertAlmostEqual(t.calculateSquare(), 3.89711431)
		
        # значение некорректное, при рассчете не может посчитать корень из отриц числа, функция calculateSquare() должна вернуть math domain error
	def testIncorrectParamInCalculateSquare(self):
                #ловим сообщние о том, что это не треугольнике		
		t = Triangle(13, -3, -3)
		self.assertEqual("not triangle", t.calculateSquare())
		t = Triangle(0, 0, 0)
		self.assertEqual("not triangle", t.calculateSquare())

	# Проверяем, что фунция calculateAngle выдает верный результат
	def testCalculateAngle(self):
		t = Triangle(2, 3, 4)
		self.assertAlmostEqual(t.calculateAngle("alpha"), 28.9550244)
		self.assertAlmostEqual(t.calculateAngle("beta"), 46.5674634)
		self.assertAlmostEqual(t.calculateAngle("gamma"), 104.4775122)
                
        #Проверяем, что фунция calculateAngle когда неккоректное название угла, возращает False
	#или когда неверные стороны возвращает not triangle
	def testIncorrectParamInCalculateAngle(self):
                #название угла неккоректно		
		t = Triangle(13, -3, -3)
		self.assertFalse(t.calculateAngle("a13lpasdha"))
		#неверные стороны
		t = Triangle(0, 0, 0)
		self.assertEqual("not triangle", t.calculateAngle("alpha"))
		
		
	# Проверяем, что фунция getType выдает верный результат
	def testGetType(self):
                #функция getType должна выдавать прямоугольный(right) тип
                #beta = 90
		t = Triangle(3, 5, 4)
		self.assertEqual("right", t.getType())
		#gamma = 90
		t = Triangle(4, 3, 5)
		self.assertEqual("right", t.getType())
                #alpha = 90
		t = Triangle(5, 3, 4)
		self.assertEqual("right", t.getType())
		#функция getType должна выдавать равнобедренный(isosceles) тип
		t = Triangle(3, 2, 2)
		self.assertEqual("isosceles", t.getType())
		t = Triangle(2, 2, 3)
		self.assertEqual("isosceles", t.getType())
		t = Triangle(2, 3, 2)
		self.assertEqual("isosceles", t.getType())
                #функция getType должна выдавать равносторонний(equilateral) тип
		t = Triangle(3, 3, 3)
		self.assertEqual("equilateral", t.getType())
                #функция getType должна выдавать просто треугольник(common) тип
		t = Triangle(2, 3, 4)
		self.assertEqual("common", t.getType())
		# значение некорректное, это не треугольник, функция getType() должна вернуть "not triangle"
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