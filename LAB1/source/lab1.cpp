/**
==============   TOLSA   ===================
===============  LAB 1  ====================
=== L(G) = {€, €€, €€€‚, €€€€‚‚,...} =
====== Author: Oleg Pedorenko, IP-31 =======
============= FICT, ASOIU ==================
========== Created on: 20.02.===============
============================================
*/

#include "iostream"
#include "string"

using namespace std;

bool matchGrammar(string s)
{
	int k = 0, l = 0, m = 0, i = 0;
	char a = 'A', b = 'B', c = 'C';
	for(i; s[i] == a && i < s.length(); i++, k++);
	for(i; s[i] == b && i < s.length(); i++, l++);
	for(i; s[i] == c && i < s.length(); i++, m++);
	//cout << k << " " << l  << " " << m << " " << s << endl;
	return ((k == l + 1) && (l == m + 1)) || (s == "A");
}

string getTestString()
{
	return "AAABBC";
}

int main(int argc, char** argv)
{
//	cout << argc << endl;
	for(int i = 1; i < argc; i++)
	{
		cout << string(argv[i]) << endl;
		if(matchGrammar(string(argv[i]))) {
			cout << "This word exists in given language" << endl;
		}
		else {
			cout << "This word does not exist in given language" << endl;
		}
	}
	return 0;
}