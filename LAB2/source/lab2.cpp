/**
==============   TOLSA   ===================
===============  LAB 2  ====================
============= Variant 16 ===================
====== Author: Oleg Pedorenko, IP-31 =======
============= FICT, ASOIU ==================
========== Created on: 23.02.2016 ==========
============================================
*/

#include "iostream"
#include "fstream"
#include "string"
#include "vector"
#include "stack"

using namespace std;

void printHelp(string exeName)
{
	cout << "=============   TOLSA   ====================\n" <<
			"===============  LAB 2  ====================\n" << 
			"============= Variant 16 ===================\n" <<
			"====== Author: Oleg Pedorenko, IP-31 =======\n" <<
			"============= FICT, ASOIU ==================\n" <<
			"========== Created on: 23.02.2016 ==========\n" <<
			"============================================\n";
	cout << endl;
	cout << "Pass the path to the file with a list of lines to\n" <<
			"analyze as a command line argument\n";
	cout << endl;
	cout << "Example:\n" << exeName << " sample.pas\n";
	cout << endl;
	cout << "Output: \nAAAABBBBCC\nThis word exists in given language\n";
	cout << endl;	
}

vector<string>* loadFile(string fileName)
{
	ifstream inputFile(fileName.c_str());
	if(!inputFile.good())
	{
		return NULL;
	}
	vector<string>* stringVector = new vector<string>();
	do
	{
		stringVector->push_back("");
		getline(inputFile, stringVector->back());
	} while (inputFile.good());
	return stringVector;
}

void printStringVector(vector<string>* stringVector, ostream& os = cout)
{
	for(string& s: *stringVector)
	{
		os << s << endl;
	}
}

int orderValue(char a)
{
	switch(a)
	{
		case '+':
		case '-':
			return 0;
			break;
		case '*':
		case '/':
			return 1;
			break;
		case '=':
			return 2;
			break;
		default:
			return -1;
	}
}

bool precedence(char a, char b)
{
	return orderValue(a) >= orderValue(b);
}

bool isOperation(char a)
{
	return orderValue(a) >= 0;
}

string infixToPostfix(string s)
{
	string postfix = "";
	stack<char> opstk;
	for(char c: s)
	{
		if(isOperation(c))
		{
			char smbtop;
			while(!opstk.empty() && precedence(smbtop = opstk.top(), c))
			{
				postfix.append(smbtop);
				opstk.pop()
			}
			opstk.push(c);
		}
		else
		{
			postfix.append(c);
		}
	}
	while(!opstk.empty())
	{
		postfix.append(opstk.top());
		opstk.pop();
	}	
}

vector<string>* stringVectorInfixToPostfix(vector<string>* stringVector)
{
	vector<string>* result = new vector<string>();
	for(string& s: *stringVector)
	{
		result->push_back(infixToPostfix(s));
	}
	return result;
}

int main(int argc, char** argv)
{
 	if(argc == 1) 
	{
		printHelp(argv[0]);
	}
	else if(argc == 2)
	{
		vector<string>* lines = loadFile(argv[1]);
		if(lines == NULL) 
		{
			cout << "i/o error\n";
		}
		else 
		{
			printStringVector(stringVectorInfixToPostfix(lines));
		}
	}
	else if(argc > 2)
	{
		cout << "Too many arguments";
	} 
}