/**
==============   TOLSA   ===================
===============  LAB 1  ====================
=== L(G) = {A, AAB, AAABBC, AAAABBBCC, ..} =
====== Author: Oleg Pedorenko, IP-31 =======
============= FICT, ASOIU ==================
========== Created on: 20.02.2016 ==========
============================================
*/

#include "iostream"
#include "string"

using namespace std;

void printHelp(string programName)
{
	cout << "=============   TOLSA   ====================\n" <<
			"===============  LAB 1  ====================\n" << 
			"=== L(G) = {A, AAB, AAABBC, AAAABBBCC, ..} =\n" <<
			"====== Author: Oleg Pedorenko, IP-31 =======\n" <<
			"============= FICT, ASOIU ==================\n" <<
			"========== Created on: 20.02.2016 ==========\n" <<
			"============================================\n";
	cout << endl;
	cout << "Pass words as command line arguments to this program to check \n" << 
			"whether these words exist in a given language L(G)\n";
	cout << endl;
	cout << "Example:\n" << programName << " AAAABBBCC\n";
	cout << endl;
	cout << "Output: \nAAAABBBBCC\nThis word does not exist in given language\n";
	cout << endl;	
}

bool matchGrammar(string s)
{
	int n[] = {0, 0, 0};
	char a[] = {'A', 'B', 'C'};
	int i = 0;
	for(int j = 0; j < 3; j++)
	{
		for(i; s[i] == a[j] && i < s.length(); i++, n[j]++);
	}
	return ((n[0] == (n[1] + 1)) && (n[1] == (n[2] + 1)))
			|| (s == "A");
}

string getTestString()
{
	return "AAABBC";
}

int main(int argc, char** argv)
{
	if(argc == 1) 
	{
		printHelp(argv[0]);
	}
	for(int i = 1; i < argc; i++)
	{
		string expression = string(argv[i]);
		cout << expression << endl;
		if(matchGrammar(expression)) 
		{
			cout << "This word exists in given language" << endl;
		}
		else 
		{
			cout << "This word does not exist in given language" << endl;
		}
	}
	return 0;
}