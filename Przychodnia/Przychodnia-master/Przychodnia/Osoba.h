#pragma once

#include <string>
#include <ostream>
using namespace std;

class Osoba
{
public:
	string imie;
	string nazwisko;
	string login;
	string haslo;
public:
	Osoba();
	Osoba(string imie, string nazwisko, string login, string haslo);	
	~Osoba();
	void ustaw(string imie, string nazwisko, string login, string haslo);
};

