#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <numeric>

#include "Rezultat.h"

using namespace std;

class Biegacz
{
	string imie;
	string nazwisko;
	string login;
	string haslo;
	vector<Rezultat*> rezultaty;
public:
	Biegacz();
	Biegacz(string imie, string nazwisko, string login, string haslo);
	~Biegacz();

	bool zaloguj(string login, string haslo);
	Bieg* wybierzBieg(vector<Bieg*>& biegi);
	void dodajRezultat(Rezultat* rezultat);
	void wyswietlRezultaty();
	void obliczSredniaPredkosc();
	void obliczPokonanyDystans();
	string imieNazwisko();

	// przeciazone funkcje (operatory)
	friend ostream& operator<< (ostream& out, const Biegacz& biegacz)
	{
		out << biegacz.imie << " " << biegacz.nazwisko << " " << biegacz.login << " " << biegacz.haslo;
		return out;
	}

	friend istream &operator>>(istream &is, Biegacz& biegacz)
	{
		is >> biegacz.imie >> biegacz.nazwisko >> biegacz.login >> biegacz.haslo;
		return is;
	}
};

