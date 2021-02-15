#pragma once

#include <ostream>
#include <istream>
#include "Bieg.h"

using namespace std;

class Rezultat
{
private:
	Bieg* bieg;
	double czas; // w sekundach
public:
	Rezultat();
	Rezultat(Bieg* bieg, double czas);
	~Rezultat();
	double Czas();
	double Dystans();
	string opis();

	// przeciazone funkcje (operatory)
	friend ostream& operator<< (ostream& out, const Rezultat& rezultat)
	{
		out << *rezultat.bieg << " " << rezultat.czas;
		return out;
	}

	friend istream &operator>>(istream &is, Rezultat& rezultat) 
	{
		is >> *rezultat.bieg >> rezultat.czas;
		return is;
	}
};

