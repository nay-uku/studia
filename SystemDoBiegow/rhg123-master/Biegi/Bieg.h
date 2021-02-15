#pragma once

#include <string>
#include <istream>

#include "Bieg.h"

using namespace std;

class Bieg
{
public:
	string nazwa;
	double dystans;
	Bieg();
	Bieg(string nazwa, double dystans);
	~Bieg();
	string opis();

	// przeciazone funkcje (operatory)
	friend ostream& operator<< (ostream& out, const Bieg& bieg)
	{
		out << bieg.nazwa << " " << bieg.dystans;
		return out;
	}

	friend istream &operator>>(istream &is, Bieg& bieg)
	{
		is >> bieg.nazwa >> bieg.dystans;
		return is;
	}
};

