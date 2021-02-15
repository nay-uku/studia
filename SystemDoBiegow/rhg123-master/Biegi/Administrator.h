#pragma once

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

#include "Biegacz.h"
#include "Bieg.h"
#include "Rezultat.h"

using namespace std;

class Administrator
{
private:
	string login;
	string haslo;
public:
	Administrator();
	Administrator(string login, string haslo);
	~Administrator();
	bool zaloguj(string login, string haslo);
	void dodajBiegacza(vector<Biegacz*>& biegacze);
	void dodajBieg(vector<Bieg*>& biegi);
	Bieg* wybierzBieg(vector<Bieg*>& biegi);
	Biegacz* wybierzBiegacza(vector<Biegacz*>& biegacze);
	void dodajRezultat(vector<Biegacz*>& biegacze, vector<Bieg*>& biegi);
	void wyswietlBiegaczy(vector<Biegacz*>& biegacze);
	void wyswietlBiegi(vector<Bieg*>& biegi);

	// przeciazone funkcje (operatory)
	friend ostream& operator<< (ostream& out, const Administrator& administrator)
	{
		out << administrator.login << " " << administrator.haslo;
		return out;
	}

	friend istream &operator>>(istream &is, Administrator& administrator)
	{
		is >> administrator.login >> administrator.haslo;
		return is;
	}
};

