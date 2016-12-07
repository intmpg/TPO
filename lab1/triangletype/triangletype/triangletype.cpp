#include "stdafx.h"
#include <string>
#include <iostream>
#include <sstream>
#include <Windows.h>
#include <vector>

using namespace std;


bool GetParametersFromCmd(const std::string & numberStr)
{
	double number = atof(numberStr.c_str());
	std::stringstream ss;
	ss << number;
	return (numberStr == ss.str());
}

bool IsParametersCorrect(int argc, char ** argv)
{
	if (argc == 4)
	{
		if (GetParametersFromCmd(argv[1]) && GetParametersFromCmd(argv[2]) && GetParametersFromCmd(argv[3]))
		{
		
			return true;	
		}
	}
	
	return false;
}

string TriangleTypeDefinition(char ** argv)
{
	
	double a = atof(argv[1]);
	double b = atof(argv[2]);
	double c = atof(argv[3]);

	string type1 = "Треугольник равносторонний";
	string type2 = "Треугольник равнобедренный";
	string type3 = "Треугольник разносторонний";
	string error = "Ошибка! Треугольник с указанными параметрами не существует!";

	
	if ((a > 0) && (b > 0) && (c > 0))
	{

		if ((a + b > c) && (b + c > a) && (a + c > b))
		{

			if ((a == b) && (b == c))
			{

				return type1;
			}
	
			else
			
			{
				if ((a == b) || (b == c) || (a == c))
				{
					return type2;
				}
			
				else
				
				{
					return type3;
				}
			}
			
		}

		else
		
		{
			return error;
		}
	}
	
	else
	
	{
		return error;
	}
}

int main(int argc, char ** argv)
{

	SetConsoleOutputCP(1251);
	SetConsoleCP(1251);

	if (IsParametersCorrect(argc, argv))
	{
		string triangleType = TriangleTypeDefinition(argv);
		std::cout << triangleType;
	}
	
	else
	
	{

		std::cout << "Ошибка! Указано меньше 3-х аргументов. Формат ввода: triangle.exe 2 2 3";
	}
}